from app.rag.vector_store import create_statement_index


def ingest_transactions(statement_id: str, transactions):

    documents = []

    for transaction in transactions:

        text = f"""
        Date: {transaction.date}
        Value Date: {transaction.value_date}
        Narration: {transaction.narration}
        Reference: {transaction.reference}
        Amount: {transaction.amount}
        Transaction Type: {transaction.transaction_type}
        Debit: {transaction.debit}
        Credit: {transaction.credit}
        Balance: {transaction.balance}
        Category: {transaction.category}
        """.strip()

        documents.append(text)

    create_statement_index(
        statement_id,
        documents,
    )