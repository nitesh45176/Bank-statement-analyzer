import re
from langchain_core.tools import tool
from collections import defaultdict
from app.rag.vector_store import search_statement as rag_search
from app.services.statement_store import StatementStore

STOP_WORDS = {
    "how", "much", "did", "i", "spend", "on", "show", "me", "my",
    "transactions", "transaction", "from", "at", "to", "what", "was",
    "any", "were", "made", "the", "a", "an", "is", "for", "with",
    "in", "of", "and", "or", "statement", "details", "find", "get",
    "list", "tell", "about", "all"
}


def _get_statement(statement_id: str):
    statement = StatementStore.get(statement_id)
    if not statement:
        raise ValueError(
            f"Statement '{statement_id}' was not found."
        )
    return statement


def _tx_prop(tx, prop: str, default=""):
    if isinstance(tx, dict):
        val = tx.get(prop, default)
    else:
        val = getattr(tx, prop, default)
    return val if val is not None else default


def _tx_float(tx, prop: str) -> float:
    val = _tx_prop(tx, prop, 0.0)
    try:
        return float(val or 0.0)
    except (ValueError, TypeError):
        return 0.0


@tool
def get_account_details(statement_id: str) -> dict:
    """
    Get account and statement details such as bank name, account number, branch, etc.
    """
    statement = _get_statement(statement_id)
    details = statement.get("account_details", {})
    if not details:
        return {
            "found": False,
            "message": "Account details are not available for this statement."
        }
    return {
        "found": True,
        "account_details": details
    }


@tool
def get_transactions(
    statement_id: str,
    transaction_type: str | None = None,
    category: str | None = None,
    merchant: str | None = None,
) -> list[dict]:
    """
    Get transactions from the bank statement, optionally filtered by transaction_type (DEBIT/CREDIT),
    category, or merchant name.
    """
    statement = _get_statement(statement_id)
    transactions = statement.get("transactions", [])
    results = []

    merchant_lower = merchant.lower().strip() if merchant else None

    for tx in transactions:
        tx_type = _tx_prop(tx, "transaction_type", "")
        tx_category = _tx_prop(tx, "category", "")
        narration = _tx_prop(tx, "narration", "")

        if transaction_type:
            if tx_type.upper() != transaction_type.upper():
                continue

        if category:
            if tx_category.lower() != category.lower():
                continue

        if merchant_lower:
            if merchant_lower not in narration.lower():
                continue

        results.append({
            "date": _tx_prop(tx, "date"),
            "narration": narration,
            "amount": _tx_float(tx, "amount"),
            "transaction_type": tx_type,
            "debit": _tx_float(tx, "debit"),
            "credit": _tx_float(tx, "credit"),
            "balance": _tx_float(tx, "balance"),
            "category": tx_category,
        })

    return results


@tool
def calculate_spending(
    statement_id: str,
    month: str | None = None,
    category: str | None = None,
    merchant: str | None = None,
) -> dict:
    """
    Calculate total debit spending from the statement.
    Optionally filter by month (YYYY-MM or Mon YYYY), category, or merchant/payee name.
    """
    statement = _get_statement(statement_id)
    transactions = statement.get("transactions", [])

    total = 0.0
    count = 0
    matched_transactions = []

    merchant_lower = merchant.lower().strip() if merchant else None
    category_lower = category.lower().strip() if category else None

    for tx in transactions:
        date = _tx_prop(tx, "date", "")
        narration = _tx_prop(tx, "narration", "")
        tx_category = _tx_prop(tx, "category", "")

        if month and not (month.lower() in date.lower()):
            continue

        if category_lower and category_lower not in tx_category.lower():
            continue

        if merchant_lower and merchant_lower not in narration.lower():
            continue

        debit = _tx_float(tx, "debit")
        if debit > 0:
            total += debit
            count += 1
            if len(matched_transactions) < 5:
                matched_transactions.append({
                    "date": date,
                    "narration": narration,
                    "amount": debit
                })

    if count == 0:
        criteria = []
        if merchant:
            criteria.append(f"merchant '{merchant}'")
        if category:
            criteria.append(f"category '{category}'")
        if month:
            criteria.append(f"month '{month}'")
        criteria_str = f" for {', '.join(criteria)}" if criteria else ""
        return {
            "found": False,
            "month": month,
            "category": category,
            "merchant": merchant,
            "total_spending": 0.0,
            "transaction_count": 0,
            "message": f"No debit transactions found{criteria_str} in this statement."
        }

    return {
        "found": True,
        "month": month,
        "category": category,
        "merchant": merchant,
        "total_spending": round(total, 2),
        "transaction_count": count,
        "sample_transactions": matched_transactions,
    }


@tool
def calculate_income(
    statement_id: str,
    source: str | None = None,
) -> dict:
    """
    Calculate total credit/income from the statement, optionally filtered by income source/payee keyword.
    """
    statement = _get_statement(statement_id)
    transactions = statement.get("transactions", [])

    total = 0.0
    count = 0
    source_lower = source.lower().strip() if source else None

    for tx in transactions:
        narration = _tx_prop(tx, "narration", "")
        if source_lower and source_lower not in narration.lower():
            continue

        credit = _tx_float(tx, "credit")
        if credit > 0:
            total += credit
            count += 1

    if count == 0:
        source_str = f" matching '{source}'" if source else ""
        return {
            "found": False,
            "source": source,
            "total_income": 0.0,
            "transaction_count": 0,
            "message": f"No credit transactions found{source_str} in this statement."
        }

    return {
        "found": True,
        "source": source,
        "total_income": round(total, 2),
        "transaction_count": count,
    }


@tool
def get_category_summary(statement_id: str) -> dict:
    """
    Calculate spending grouped by transaction category.
    """
    statement = _get_statement(statement_id)
    transactions = statement.get("transactions", [])

    summary = defaultdict(float)

    for tx in transactions:
        debit = _tx_float(tx, "debit")
        category = _tx_prop(tx, "category", "Uncategorized")
        if debit > 0:
            summary[category] += debit

    if not summary:
        return {
            "found": False,
            "message": "No categorized debit transactions found in this statement.",
            "categories": {}
        }

    return {
        "found": True,
        "categories": {
            category: round(amount, 2)
            for category, amount in summary.items()
        }
    }


@tool
def get_monthly_summary(statement_id: str) -> dict:
    """
    Calculate monthly debit and credit totals.
    """
    statement = _get_statement(statement_id)
    transactions = statement.get("transactions", [])

    result = defaultdict(
        lambda: {
            "debit": 0.0,
            "credit": 0.0,
            "count": 0,
        }
    )

    for tx in transactions:
        date = _tx_prop(tx, "date", "")
        month = date[:7] if len(date) >= 7 else "Unknown"

        result[month]["debit"] += _tx_float(tx, "debit")
        result[month]["credit"] += _tx_float(tx, "credit")
        result[month]["count"] += 1

    if not result:
        return {
            "found": False,
            "message": "No monthly data found in this statement.",
            "monthly": {}
        }

    return {
        "found": True,
        "monthly": {
            month: {
                "debit": round(values["debit"], 2),
                "credit": round(values["credit"], 2),
                "count": values["count"],
            }
            for month, values in result.items()
        }
    }


@tool
def search_statement(
    statement_id: str,
    query: str,
) -> list[str]:
    """
    Search the uploaded bank statement for specific transactions, merchants, narrations,
    or reference numbers.
    """
    raw_query = query.strip()
    query_lower = raw_query.lower()

    # Extract meaningful search terms excluding generic stop words
    tokens = [
        t for t in re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", query_lower)
        if t not in STOP_WORDS
    ]

    # 1. Direct transaction matching first (precise and zero false positives)
    try:
        statement = _get_statement(statement_id)
        transactions = statement.get("transactions", [])
        if not transactions:
            return []

        scored = []
        for tx in transactions:
            narration = _tx_prop(tx, "narration", "").lower()
            category = _tx_prop(tx, "category", "").lower()
            ref = _tx_prop(tx, "reference", "").lower()
            date = _tx_prop(tx, "date", "").lower()
            tx_type = _tx_prop(tx, "transaction_type", "").lower()

            score = 0

            # Exact phrase match in narration
            if query_lower in narration:
                score += 30

            # Meaningful tokens matching
            for token in tokens:
                if token in narration:
                    score += 15
                elif token in category:
                    score += 8
                elif token in ref:
                    score += 10
                elif token in date:
                    score += 5

            if score > 0:
                scored.append((score, tx))

        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            top_matches = [tx for _, tx in scored[:7]]

            documents = []
            for tx in top_matches:
                doc = f"""
Date: {_tx_prop(tx, 'date')}
Value Date: {_tx_prop(tx, 'value_date')}
Narration: {_tx_prop(tx, 'narration')}
Reference: {_tx_prop(tx, 'reference')}
Amount: {_tx_float(tx, 'amount')}
Transaction Type: {_tx_prop(tx, 'transaction_type')}
Debit: {_tx_float(tx, 'debit')}
Credit: {_tx_float(tx, 'credit')}
Balance: {_tx_float(tx, 'balance')}
Category: {_tx_prop(tx, 'category')}
                """.strip()
                documents.append(doc)
            return documents

    except Exception as e:
        print(f"[search_statement] Direct search error: {e}")

    # 2. Try vector/RAG search only if tokens exist and direct search found nothing
    try:
        results = rag_search(
            statement_id,
            query,
            k=5,
        )
        if results:
            # Verify RAG results actually match at least one search token to avoid false positives
            if tokens:
                verified = []
                for doc in results:
                    doc_lower = doc.lower()
                    if any(token in doc_lower for token in tokens):
                        verified.append(doc)
                if verified:
                    return verified
            else:
                return results
    except Exception as e:
        print(f"[search_statement] RAG search error: {e}")

    # If no matches were found anywhere, return empty list (valid zero-match)
    return []