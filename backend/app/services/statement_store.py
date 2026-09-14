"""
StatementStore — thin in-memory cache backed by SQLite via the repository layer.

The rest of the application (tools, API routes) continues to call:
    StatementStore.save(statement_id, data)
    StatementStore.get(statement_id)
    StatementStore.delete(statement_id)

Internally this now delegates to app.database.repository for persistence.
"""
from typing import Any
from app.database import repository


class StatementStore:

    # In-process cache so repeated tool calls don't round-trip to SQLite.
    _cache: dict[str, dict[str, Any]] = {}

    @classmethod
    def save(cls, statement_id: str, data: dict[str, Any]):
        """
        Persist statement to SQLite and warm the in-memory cache.

        data must contain:
            "transactions": list[Transaction | dict]
            "account_details": dict
        Optionally:
            "detected_bank": str
        """
        cls._cache[statement_id] = data

        try:
            repository.save_statement(
                statement_id=statement_id,
                bank=data.get("detected_bank", ""),
                account_details=data.get("account_details", {}),
                transactions=data.get("transactions", []),
            )
        except Exception as e:
            print(f"[StatementStore] Warning: SQLite persist failed: {e}")

    @classmethod
    def get(cls, statement_id: str) -> dict[str, Any] | None:
        # Return from cache if available
        if statement_id in cls._cache:
            return cls._cache[statement_id]

        # Load from SQLite
        data = repository.get_statement(statement_id)
        if data:
            cls._cache[statement_id] = data
        return data

    @classmethod
    def delete(cls, statement_id: str):
        cls._cache.pop(statement_id, None)
        repository.delete_statement(statement_id)