"""
Repository functions for Statement and Transaction persistence.
All database access in the application goes through this module.
"""
import json
import uuid
from dataclasses import asdict, is_dataclass

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import StatementModel, TransactionModel
from app.models.transaction import Transaction


# ── helpers ─────────────────────────────────────────────────────────────────

def _session() -> Session:
    return SessionLocal()


def _tx_to_model(statement_id: str, idx: int, tx) -> TransactionModel:
    """Convert a Transaction dataclass or dict to a TransactionModel row."""
    if is_dataclass(tx):
        d = asdict(tx)
    elif isinstance(tx, dict):
        d = tx
    else:
        d = getattr(tx, "__dict__", {})

    return TransactionModel(
        id=f"{statement_id}_{idx}",
        statement_id=statement_id,
        date=d.get("date", ""),
        value_date=d.get("value_date", ""),
        narration=d.get("narration", ""),
        reference=d.get("reference", ""),
        amount=float(d.get("amount") or 0.0),
        transaction_type=d.get("transaction_type") or "UNKNOWN",
        debit=float(d.get("debit") or 0.0),
        credit=float(d.get("credit") or 0.0),
        balance=float(d.get("balance") or 0.0),
        category=d.get("category") or "Uncategorized",
    )


def _model_to_tx(row: TransactionModel) -> Transaction:
    return Transaction(
        date=row.date or "",
        value_date=row.value_date or "",
        narration=row.narration or "",
        reference=row.reference or "",
        amount=row.amount or 0.0,
        transaction_type=row.transaction_type or "UNKNOWN",
        debit=row.debit or 0.0,
        credit=row.credit or 0.0,
        balance=row.balance or 0.0,
        category=row.category or "Uncategorized",
    )


# ── public API ───────────────────────────────────────────────────────────────

def save_statement(
    statement_id: str,
    bank: str,
    account_details: dict,
    transactions: list,
):
    """Persist statement metadata and all transactions. Replaces existing rows."""
    db = _session()
    try:
        # Upsert statement
        existing = db.get(StatementModel, statement_id)
        if existing:
            existing.bank = bank
            existing.account_details = json.dumps(account_details, ensure_ascii=False)
        else:
            db.add(StatementModel(
                statement_id=statement_id,
                bank=bank,
                account_details=json.dumps(account_details, ensure_ascii=False),
            ))

        # Delete old transactions then re-insert
        db.query(TransactionModel).filter(
            TransactionModel.statement_id == statement_id
        ).delete()

        for idx, tx in enumerate(transactions):
            db.add(_tx_to_model(statement_id, idx, tx))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[repository] save_statement error: {e}")
        raise
    finally:
        db.close()


def get_statement(statement_id: str) -> dict | None:
    """
    Return {account_details: dict, transactions: list[Transaction]} or None.
    Same shape as the old StatementStore.get() result.
    """
    db = _session()
    try:
        row = db.get(StatementModel, statement_id)
        if not row:
            return None

        account_details = {}
        if row.account_details:
            try:
                account_details = json.loads(row.account_details)
            except Exception:
                pass

        tx_rows = (
            db.query(TransactionModel)
            .filter(TransactionModel.statement_id == statement_id)
            .all()
        )
        transactions = [_model_to_tx(r) for r in tx_rows]

        return {
            "account_details": account_details,
            "transactions": transactions,
        }
    finally:
        db.close()


def delete_statement(statement_id: str):
    db = _session()
    try:
        row = db.get(StatementModel, statement_id)
        if row:
            db.delete(row)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"[repository] delete_statement error: {e}")
    finally:
        db.close()


def get_transactions(statement_id: str) -> list[Transaction]:
    db = _session()
    try:
        rows = (
            db.query(TransactionModel)
            .filter(TransactionModel.statement_id == statement_id)
            .all()
        )
        return [_model_to_tx(r) for r in rows]
    finally:
        db.close()
