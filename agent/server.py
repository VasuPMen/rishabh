"""
FastAPI server exposing the Customer Billing Review Agent as an HTTP API.
Consumed by the CAP backend proxy.
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Load environment variables from .env
load_dotenv(Path(__file__).resolve().parent / ".env")

from agent import run_agent
from mock_data import CUSTOMERS, CUSTOMER_NAME_INDEX

app = FastAPI(title="Customer Billing Review Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    history: list[dict]


@app.get("/health")
def health():
    return {"status": "ok", "service": "Customer Billing Review Agent"}


@app.get("/customers")
def list_customers():
    """Return the list of available mock customers."""
    return [{"id": k, "name": v["name"]} for k, v in CUSTOMERS.items()]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Send a message to the agent and receive a response.
    Optionally pre-inject the customer context into the first user message.
    """
    # Build history from request
    history = [{"role": m.role, "content": m.content} for m in req.history]

    # Compose user message, optionally enriched with customer context
    user_content = req.message
    if (req.customer_id or req.customer_name) and not history:
        ctx_parts = []
        if req.customer_id:
            ctx_parts.append(f"Customer ID: {req.customer_id}")
        if req.customer_name:
            ctx_parts.append(f"Customer Name: {req.customer_name}")
        user_content = f"[Context: {', '.join(ctx_parts)}]\n\n{req.message}"

    history.append({"role": "user", "content": user_content})

    try:
        result = run_agent(history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Return only clean user and assistant conversation turns
    clean_history = [
        {"role": m.get("role"), "content": m.get("content")}
        for m in result["messages"]
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]

    return ChatResponse(response=result["response"], history=clean_history)


if __name__ == "__main__":
    import uvicorn
    # Cloud Foundry assigns PORT dynamically; default to 8000 locally
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
