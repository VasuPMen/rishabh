# Customer Billing Review Agent

A read-only AI agent that helps billing specialists review customer accounts by retrieving billing data and contract information, comparing payment behaviour against contractual obligations, and generating a Customer Billing Review Summary.

## Solution Structure

```
├── agent/          Python AI agent + FastAPI server
├── backend/        CAP (Node.js) backend that proxies to the agent
└── ui/             React + SAP UI5 Web Components frontend
```

## Quick Start (Local Development)

### 1. Configure the AI credentials

```bash
cp agent/.env.example agent/.env
# Edit agent/.env and add your SAP AI Core or OpenAI credentials
```

### 2. Start the Python agent

```bash
cd agent
pip install -r requirements.txt
python server.py
# Runs on http://localhost:8000
```

### 3. Start the CAP backend

```bash
cd backend
npm install
AGENT_BASE_URL=http://localhost:8000 npm run dev
# Runs on http://localhost:4004
```

### 4. Start the UI (development)

```bash
cd ui
npm install
npm run dev
# Opens at http://localhost:5173
```

## Demo Customers

| ID   | Name                   | Scenario                                              |
|------|------------------------|-------------------------------------------------------|
| C001 | Horizon Tech GmbH      | Consistently late payments (~12 days), 2 overdue invoices |
| C002 | BlueSky Logistics AG   | Excellent payer — pays early, low credit utilisation  |
| C003 | Nordic Retail Group    | High risk — 4 overdue invoices, credit limit exceeded |
| C004 | Vesta Manufacturing Ltd| Perfect payment record, Net 60 terms                  |
| C005 | Eastbridge Consulting  | Minor delays, 1 small overdue invoice                 |

## Agent Capabilities

**Can do:**
- Retrieve billing information (invoices, balances, payment history)
- Retrieve contract information (payment terms, credit limits, arrangements)
- Compare payment behaviour against contract terms
- Identify discrepancies and generate a review summary
- Recommend whether the account needs further review

**Cannot do:**
- Modify invoices, contracts, or account data
- Apply credits, write-offs, or adjustments
- Change payment terms or credit limits
- Initiate collections activities

## Production Integration

Replace the mock data in `agent/mock_data.py` with real API calls to your billing and contract management systems (e.g. SAP S/4HANA Accounts Receivable, SAP Contract Management).
