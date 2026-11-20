"""
Agent tools for the Customer Billing Review Agent.
Each tool is a plain Python function; the agent calls them via OpenAI function-calling.
"""
import json
from mock_data import (
    CUSTOMERS,
    CUSTOMER_NAME_INDEX,
    BILLING_DATA,
    CONTRACT_DATA,
)


def resolve_customer(customer_id: str = None, customer_name: str = None) -> dict:
    """
    Resolve a customer record by ID or name.
    Returns {"customer_id": ..., "customer_name": ...} or an error dict.
    """
    if customer_id:
        cid = customer_id.upper().strip()
        if cid in CUSTOMERS:
            return {"customer_id": cid, "customer_name": CUSTOMERS[cid]["name"]}
        return {"error": f"No customer found with ID '{customer_id}'."}

    if customer_name:
        key = customer_name.lower().strip()
        # Exact match first
        if key in CUSTOMER_NAME_INDEX:
            cid = CUSTOMER_NAME_INDEX[key]
            return {"customer_id": cid, "customer_name": CUSTOMERS[cid]["name"]}
        # Partial match
        matches = [
            {"customer_id": CUSTOMERS[cid]["id"], "customer_name": CUSTOMERS[cid]["name"]}
            for name_key, cid in CUSTOMER_NAME_INDEX.items()
            if key in name_key
        ]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            return {"error": "Multiple customers matched. Please be more specific.", "matches": matches}
        return {"error": f"No customer found with name '{customer_name}'."}

    return {"error": "Please provide either a customer_id or customer_name."}


def get_billing_information(customer_id: str = None, customer_name: str = None) -> str:
    """
    Retrieve billing information for a customer: outstanding invoices,
    overdue balances, payment history, and average payment behaviour.
    """
    resolved = resolve_customer(customer_id, customer_name)
    if "error" in resolved:
        return json.dumps(resolved)

    cid = resolved["customer_id"]
    data = BILLING_DATA.get(cid)
    if not data:
        return json.dumps({"error": f"No billing data found for customer {cid}."})
    return json.dumps(data, indent=2)


def get_contract_information(customer_id: str = None, customer_name: str = None) -> str:
    """
    Retrieve contract information for a customer: agreed payment terms,
    credit limit, credit utilisation, and special payment arrangements.
    """
    resolved = resolve_customer(customer_id, customer_name)
    if "error" in resolved:
        return json.dumps(resolved)

    cid = resolved["customer_id"]
    data = CONTRACT_DATA.get(cid)
    if not data:
        return json.dumps({"error": f"No contract data found for customer {cid}."})
    return json.dumps(data, indent=2)


def compare_payment_behavior(customer_id: str = None, customer_name: str = None) -> str:
    """
    Compare actual payment behaviour against contractual payment terms.
    Returns a structured comparison with discrepancy flags.
    """
    resolved = resolve_customer(customer_id, customer_name)
    if "error" in resolved:
        return json.dumps(resolved)

    cid = resolved["customer_id"]
    billing = BILLING_DATA.get(cid)
    contract = CONTRACT_DATA.get(cid)

    if not billing or not contract:
        return json.dumps({"error": f"Insufficient data for comparison for customer {cid}."})

    payment_days = contract["payment_days"]
    avg_late = billing["average_days_late"]
    effective_avg_days = payment_days + avg_late  # actual average days to pay from invoice date

    overdue_invoices = [inv for inv in billing["outstanding_invoices"] if inv["status"] == "Overdue"]
    credit_exceeded = billing["total_outstanding"] > contract["credit_limit"]

    discrepancies = []

    if avg_late > 0:
        discrepancies.append({
            "type": "Late Payment Pattern",
            "detail": (
                f"Contract specifies {payment_days}-day payment terms. "
                f"Customer's average payment is {avg_late:.1f} days late, "
                f"resulting in an effective average of {effective_avg_days:.1f} days to pay."
            ),
            "severity": "High" if avg_late > 20 else "Medium" if avg_late > 7 else "Low",
        })

    if overdue_invoices:
        total_overdue_amt = sum(inv["amount"] for inv in overdue_invoices)
        discrepancies.append({
            "type": "Overdue Invoices",
            "detail": (
                f"{len(overdue_invoices)} invoice(s) totalling {total_overdue_amt:,.2f} {billing['currency']} "
                f"are currently overdue."
            ),
            "severity": "High" if total_overdue_amt > 20000 else "Medium",
            "invoices": [{"id": inv["invoice_id"], "amount": inv["amount"], "days_overdue": inv["days_overdue"]} for inv in overdue_invoices],
        })

    if credit_exceeded:
        discrepancies.append({
            "type": "Credit Limit Exceeded",
            "detail": (
                f"Current exposure of {billing['total_outstanding']:,.2f} {billing['currency']} "
                f"exceeds the agreed credit limit of {contract['credit_limit']:,.2f} {billing['currency']} "
                f"by {billing['total_outstanding'] - contract['credit_limit']:,.2f} {billing['currency']}."
            ),
            "severity": "High",
        })

    if not discrepancies:
        discrepancies.append({
            "type": "No Discrepancies",
            "detail": "Payment behaviour is in line with contractual terms.",
            "severity": "None",
        })

    comparison = {
        "customer_id": cid,
        "customer_name": resolved["customer_name"],
        "contract_payment_terms": contract["payment_terms"],
        "contracted_payment_days": payment_days,
        "average_days_late": avg_late,
        "effective_average_payment_days": effective_avg_days,
        "total_outstanding": billing["total_outstanding"],
        "total_overdue": billing["total_overdue"],
        "credit_limit": contract["credit_limit"],
        "credit_utilization_pct": contract["credit_utilization_pct"],
        "credit_limit_exceeded": credit_exceeded,
        "discrepancies": discrepancies,
        "discrepancy_count": len([d for d in discrepancies if d["type"] != "No Discrepancies"]),
        "currency": billing["currency"],
    }
    return json.dumps(comparison, indent=2)


# ── Tool definitions for OpenAI function-calling ──────────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_billing_information",
            "description": (
                "Retrieve billing information for a customer. "
                "Returns outstanding invoices, overdue balances, payment history, "
                "and average payment behaviour. "
                "Use this whenever the user asks about invoices, balances, or payment history."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer's unique ID (e.g. C001).",
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "The customer's full or partial name.",
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_contract_information",
            "description": (
                "Retrieve contract information for a customer. "
                "Returns agreed payment terms, credit limit, credit utilisation, "
                "and any special payment arrangements. "
                "Use this whenever the user asks about contract terms, credit limits, or agreements."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer's unique ID (e.g. C001).",
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "The customer's full or partial name.",
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_payment_behavior",
            "description": (
                "Compare a customer's actual payment behaviour against their contractual payment terms. "
                "Identifies discrepancies such as late payments, overdue invoices, and credit limit breaches. "
                "Use this to generate a full billing review comparison or when the user asks about variances."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer's unique ID (e.g. C001).",
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "The customer's full or partial name.",
                    },
                },
                "additionalProperties": False,
            },
        },
    },
]

TOOL_MAP = {
    "get_billing_information": get_billing_information,
    "get_contract_information": get_contract_information,
    "compare_payment_behavior": compare_payment_behavior,
}
