from langchain_core.messages import HumanMessage

from app.agent.graph import graph
from app.agent.state import AgentState
from app.services.statement_store import StatementStore
from app.models.transaction import Transaction
from app.rag.ingest import ingest_transactions

transactions = [
    Transaction(
        date="2026-06-01",
        value_date="2026-06-01",
        narration="Swiggy",
        reference="REF001",
        amount=500,
        transaction_type="DEBIT",
        debit=500,
        credit=0,
        balance=10000,
        category="Food",
    ),
    Transaction(
        date="2026-06-02",
        value_date="2026-06-02",
        narration="Salary",
        reference="REF002",
        amount=30000,
        transaction_type="CREDIT",
        debit=0,
        credit=30000,
        balance=40000,
        category="Income",
    ),
]


statement_id = "test-statement-001"


StatementStore.save(
    statement_id,
    {
        "transactions": transactions,
        "account_details": {
            "bank": "HDFC",
            "account_type": "Savings",
        },
    },
)

ingest_transactions(
    statement_id,
    transactions,
)


state: AgentState = {
    "statement_id": statement_id,
    "user_query": "What transaction was made at Swiggy?",
    "messages": [
        HumanMessage(
            content=f"""
Statement ID: {statement_id}

Question:
What transaction was made at Swiggy?
"""
        )
    ],
}


result = graph.invoke(state)


print("\n========== FINAL MESSAGES ==========\n")

for message in result["messages"]:
    print(type(message).__name__)
    print(message.content)

    if hasattr(message, "tool_calls"):
        print("TOOL CALLS:", message.tool_calls)

    print("-----------------------------------")