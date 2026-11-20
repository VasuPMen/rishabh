"""
Mock data store for the Customer Billing Review Agent.
Simulates billing and contract records for demonstration purposes.
Replace with real system integrations when going to production.
"""

CUSTOMERS = {
    "C001": {"id": "C001", "name": "Horizon Tech GmbH"},
    "C002": {"id": "C002", "name": "BlueSky Logistics AG"},
    "C003": {"id": "C003", "name": "Nordic Retail Group"},
    "C004": {"id": "C004", "name": "Vesta Manufacturing Ltd"},
    "C005": {"id": "C005", "name": "Eastbridge Consulting"},
}

# Map names (lowercase) to IDs for lookup by name
CUSTOMER_NAME_INDEX = {v["name"].lower(): k for k, v in CUSTOMERS.items()}

BILLING_DATA = {
    "C001": {
        "customer_id": "C001",
        "customer_name": "Horizon Tech GmbH",
        "outstanding_invoices": [
            {"invoice_id": "INV-10021", "amount": 12500.00, "due_date": "2024-10-15", "status": "Overdue", "days_overdue": 25},
            {"invoice_id": "INV-10034", "amount": 8750.00,  "due_date": "2024-10-30", "status": "Overdue", "days_overdue": 10},
            {"invoice_id": "INV-10047", "amount": 15200.00, "due_date": "2024-11-20", "status": "Open",    "days_overdue": 0},
        ],
        "total_outstanding": 36450.00,
        "total_overdue": 21250.00,
        "payment_history": [
            {"invoice_id": "INV-9985", "amount": 9000.00,  "due_date": "2024-08-15", "paid_date": "2024-09-02", "days_late": 18},
            {"invoice_id": "INV-9971", "amount": 11000.00, "due_date": "2024-07-30", "paid_date": "2024-08-20", "days_late": 21},
            {"invoice_id": "INV-9950", "amount": 7500.00,  "due_date": "2024-06-30", "paid_date": "2024-07-05", "days_late": 5},
            {"invoice_id": "INV-9930", "amount": 13000.00, "due_date": "2024-05-31", "paid_date": "2024-06-14", "days_late": 14},
            {"invoice_id": "INV-9910", "amount": 9500.00,  "due_date": "2024-04-30", "paid_date": "2024-05-02", "days_late": 2},
        ],
        "average_days_late": 12.0,
        "currency": "EUR",
    },
    "C002": {
        "customer_id": "C002",
        "customer_name": "BlueSky Logistics AG",
        "outstanding_invoices": [
            {"invoice_id": "INV-20011", "amount": 5300.00, "due_date": "2024-11-05", "status": "Open", "days_overdue": 0},
        ],
        "total_outstanding": 5300.00,
        "total_overdue": 0.00,
        "payment_history": [
            {"invoice_id": "INV-19998", "amount": 4800.00, "due_date": "2024-10-10", "paid_date": "2024-10-09", "days_late": -1},
            {"invoice_id": "INV-19980", "amount": 6200.00, "due_date": "2024-09-10", "paid_date": "2024-09-08", "days_late": -2},
            {"invoice_id": "INV-19965", "amount": 5100.00, "due_date": "2024-08-10", "paid_date": "2024-08-11", "days_late": 1},
        ],
        "average_days_late": -0.7,
        "currency": "EUR",
    },
    "C003": {
        "customer_id": "C003",
        "customer_name": "Nordic Retail Group",
        "outstanding_invoices": [
            {"invoice_id": "INV-30055", "amount": 22000.00, "due_date": "2024-09-01", "status": "Overdue", "days_overdue": 60},
            {"invoice_id": "INV-30066", "amount": 18500.00, "due_date": "2024-09-15", "status": "Overdue", "days_overdue": 46},
            {"invoice_id": "INV-30077", "amount": 14000.00, "due_date": "2024-10-01", "status": "Overdue", "days_overdue": 30},
            {"invoice_id": "INV-30088", "amount": 9500.00,  "due_date": "2024-10-20", "status": "Overdue", "days_overdue": 11},
        ],
        "total_outstanding": 64000.00,
        "total_overdue": 64000.00,
        "payment_history": [
            {"invoice_id": "INV-30040", "amount": 20000.00, "due_date": "2024-07-15", "paid_date": "2024-08-20", "days_late": 36},
            {"invoice_id": "INV-30030", "amount": 17000.00, "due_date": "2024-06-15", "paid_date": "2024-07-18", "days_late": 33},
        ],
        "average_days_late": 34.5,
        "currency": "EUR",
    },
    "C004": {
        "customer_id": "C004",
        "customer_name": "Vesta Manufacturing Ltd",
        "outstanding_invoices": [
            {"invoice_id": "INV-40021", "amount": 31000.00, "due_date": "2024-11-10", "status": "Open", "days_overdue": 0},
            {"invoice_id": "INV-40022", "amount": 28000.00, "due_date": "2024-11-25", "status": "Open", "days_overdue": 0},
        ],
        "total_outstanding": 59000.00,
        "total_overdue": 0.00,
        "payment_history": [
            {"invoice_id": "INV-40010", "amount": 27000.00, "due_date": "2024-10-10", "paid_date": "2024-10-10", "days_late": 0},
            {"invoice_id": "INV-40001", "amount": 25000.00, "due_date": "2024-09-10", "paid_date": "2024-09-10", "days_late": 0},
        ],
        "average_days_late": 0.0,
        "currency": "EUR",
    },
    "C005": {
        "customer_id": "C005",
        "customer_name": "Eastbridge Consulting",
        "outstanding_invoices": [
            {"invoice_id": "INV-50031", "amount": 4200.00, "due_date": "2024-10-25", "status": "Overdue", "days_overdue": 6},
        ],
        "total_outstanding": 4200.00,
        "total_overdue": 4200.00,
        "payment_history": [
            {"invoice_id": "INV-50020", "amount": 3900.00, "due_date": "2024-09-25", "paid_date": "2024-09-27", "days_late": 2},
            {"invoice_id": "INV-50010", "amount": 4100.00, "due_date": "2024-08-25", "paid_date": "2024-09-01", "days_late": 7},
        ],
        "average_days_late": 4.5,
        "currency": "EUR",
    },
}

CONTRACT_DATA = {
    "C001": {
        "customer_id": "C001",
        "customer_name": "Horizon Tech GmbH",
        "contract_id": "CON-C001-2023",
        "payment_terms": "Net 30",
        "payment_days": 30,
        "credit_limit": 50000.00,
        "current_exposure": 36450.00,
        "credit_utilization_pct": 72.9,
        "special_arrangements": "Volume discount of 5% applied on orders above EUR 10,000.",
        "account_status": "Active",
        "contract_start": "2023-01-01",
        "contract_end": "2025-12-31",
        "currency": "EUR",
    },
    "C002": {
        "customer_id": "C002",
        "customer_name": "BlueSky Logistics AG",
        "contract_id": "CON-C002-2022",
        "payment_terms": "Net 45",
        "payment_days": 45,
        "credit_limit": 30000.00,
        "current_exposure": 5300.00,
        "credit_utilization_pct": 17.7,
        "special_arrangements": "Early payment discount of 2% if paid within 10 days.",
        "account_status": "Active",
        "contract_start": "2022-06-01",
        "contract_end": "2026-05-31",
        "currency": "EUR",
    },
    "C003": {
        "customer_id": "C003",
        "customer_name": "Nordic Retail Group",
        "contract_id": "CON-C003-2023",
        "payment_terms": "Net 30",
        "payment_days": 30,
        "credit_limit": 60000.00,
        "current_exposure": 64000.00,
        "credit_utilization_pct": 106.7,
        "special_arrangements": "None",
        "account_status": "Active",
        "contract_start": "2023-03-01",
        "contract_end": "2025-02-28",
        "currency": "EUR",
    },
    "C004": {
        "customer_id": "C004",
        "customer_name": "Vesta Manufacturing Ltd",
        "contract_id": "CON-C004-2021",
        "payment_terms": "Net 60",
        "payment_days": 60,
        "credit_limit": 100000.00,
        "current_exposure": 59000.00,
        "credit_utilization_pct": 59.0,
        "special_arrangements": "Dedicated account manager assigned. Quarterly billing cycle agreed.",
        "account_status": "Active",
        "contract_start": "2021-09-01",
        "contract_end": "2026-08-31",
        "currency": "EUR",
    },
    "C005": {
        "customer_id": "C005",
        "customer_name": "Eastbridge Consulting",
        "contract_id": "CON-C005-2024",
        "payment_terms": "Net 15",
        "payment_days": 15,
        "credit_limit": 10000.00,
        "current_exposure": 4200.00,
        "credit_utilization_pct": 42.0,
        "special_arrangements": "None",
        "account_status": "Active",
        "contract_start": "2024-01-01",
        "contract_end": "2024-12-31",
        "currency": "EUR",
    },
}
