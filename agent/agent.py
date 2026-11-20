"""
Customer Billing Review Agent — core agent loop.
Uses OpenAI-compatible function calling with a ReAct-style loop.
"""
import json
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv(Path(__file__).resolve().parent / ".env")

from tools import TOOL_DEFINITIONS, TOOL_MAP

SYSTEM_PROMPT = """You are the Customer Billing Review Agent — a read-only assistant for billing specialists.

Your job is to help billing specialists review a customer's account by retrieving billing data and contract information, comparing payment behaviour against contractual obligations, and generating a clear Customer Billing Review Summary.

## Tools available
- **get_billing_information**: Retrieve outstanding invoices, overdue balances, and payment history.
- **get_contract_information**: Retrieve agreed payment terms, credit limits, and special arrangements.
- **compare_payment_behavior**: Compare actual payment behaviour against contract terms and identify discrepancies.

## Workflow
When asked to review a customer account:
1. Call `compare_payment_behavior` to get the full comparison (this internally uses both billing and contract data).
2. If the user asks for more detail on billing or contracts specifically, call the respective tool.
3. Produce a **Customer Billing Review Summary** structured as follows:

---
## Customer Billing Review Summary

**Customer:** [Name] ([ID])
**Contract:** [Contract ID] | Payment Terms: [Terms] | Credit Limit: [Amount] [Currency]

### Account Overview
- Total Outstanding: [amount]
- Total Overdue: [amount]
- Credit Utilisation: [%]
- Average Payment Time: [X] days (contracted: [Y] days)

### Discrepancies Found
[List each discrepancy with severity: High / Medium / Low]

### Special Arrangements
[Any special payment arrangements on file]

### Recommendation
[One of: ✅ No action required | ⚠️ Monitor closely | 🔴 Escalate for review]
[Brief explanation of the recommendation]

---

## Boundaries — you MUST NOT:
- Modify invoices, contracts, or any account data.
- Apply credits, write-offs, or adjustments.
- Change payment terms, credit limits, or payment arrangements.
- Initiate collections or any account actions.
- Speculate beyond the data returned by your tools.

If asked to perform any of the above, politely decline and explain that your role is read-only analysis.
Always be concise, professional, and focused on helping the billing specialist make an informed decision.
"""


def sanitize_messages(messages: list) -> list:
    """
    Ensure the message history is valid for OpenAI function calling.
    - Preserves system, user, and assistant messages.
    - Only keeps 'tool' messages if the immediately preceding message was an assistant message with 'tool_calls'.
    - Drops any orphaned 'tool' messages or assistant messages without content/tool_calls.
    """
    sanitized = []
    for msg in messages:
        role = msg.get("role")
        if role in ("system", "user"):
            sanitized.append(msg)
        elif role == "assistant":
            # Keep assistant messages if they have content or tool_calls
            if msg.get("content") or msg.get("tool_calls"):
                sanitized.append(msg)
        elif role == "tool":
            # Only keep tool message if preceding message has tool_calls
            if sanitized and sanitized[-1].get("role") == "assistant" and sanitized[-1].get("tool_calls"):
                sanitized.append(msg)
            # Otherwise drop orphaned tool message
    return sanitized


def run_agent(messages: list, model: str = None) -> dict:
    """
    Run one full agent turn given a conversation history.
    Returns {"response": str, "messages": updated_messages}.
    """
    api_key = os.environ.get("AICORE_API_KEY") or os.environ.get("OPENAI_API_KEY")
    base_url = (
        os.environ.get("AICORE_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or os.environ.get("base_url")
        or None
    )
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    model = model or os.environ.get("OPENAI_MODEL", "gpt-4o")

    # Sanitize incoming history
    messages = sanitize_messages(messages)

    # Prepend system message if not already present
    if not messages or messages[0].get("role") != "system":
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    MAX_ITERATIONS = 10
    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )

        msg = response.choices[0].message

        # Append assistant message
        messages.append(msg.model_dump(exclude_none=True))

        # If no tool calls → final answer
        if not msg.tool_calls:
            return {"response": msg.content, "messages": messages}

        # Execute each tool call
        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)

            if fn_name in TOOL_MAP:
                result = TOOL_MAP[fn_name](**fn_args)
            else:
                result = json.dumps({"error": f"Unknown tool: {fn_name}"})

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })

    return {"response": "I was unable to complete the analysis. Please try again.", "messages": messages}
