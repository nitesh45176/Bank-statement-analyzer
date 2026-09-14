from app.services.statement_store import StatementStore
from app.agent.tools import (
    calculate_spending,
    calculate_income,
    get_category_summary,
)

from app.models.transaction import Transaction


transactions = [
    Transaction(
        date="2026-06-01",
        value_date="2026-06-01",
        narration="SWIGGY FOOD",
        reference="123",
        amount=500,
        debit=500,
        credit=0,
        balance=9500,
        transaction_type="DEBIT",
        category="Food",
    ),
    Transaction(
        date="2026-06-02",
        value_date="2026-06-02",
        narration="SALARY",
        reference="456",
        amount=30000,
        debit=0,
        credit=30000,
        balance=39500,
        transaction_type="CREDIT",
        category="Salary",
    ),
]


StatementStore.save(
    "test123",
    {
        "transactions": transactions,
        "account_details": {
            "bank": "HDFC Bank"
        }
    }
)


print(calculate_spending.invoke({
    "statement_id": "test123"
}))

print(calculate_income.invoke({
    "statement_id": "test123"
}))

print(get_category_summary.invoke({
    "statement_id": "test123"
}))