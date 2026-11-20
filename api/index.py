import sys
import os
from pathlib import Path

# Add project root and agent directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
agent_dir = root_dir / "agent"
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(agent_dir))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

# Load .env if present
load_dotenv(root_dir / ".env")
load_dotenv(agent_dir / ".env")

from agent import run_agent
from mock_data import CUSTOMERS

app = FastAPI(title="Customer Billing Review Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
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
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Customer Billing Review Agent"}


@app.get("/customers")
@app.get("/api/customers")
@app.get("/customers()")
@app.get("/api/customers()")
def list_customers():
    return [{"id": k, "name": v["name"]} for k, v in CUSTOMERS.items()]


@app.post("/chat", response_model=ChatResponse)
@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    history = [{"role": m.role, "content": m.content} for m in req.history]

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

    clean_history = [
        {"role": m.get("role"), "content": m.get("content")}
        for m in result["messages"]
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]

    return ChatResponse(response=result["response"], history=clean_history)

