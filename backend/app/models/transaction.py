from dataclasses import dataclass

@dataclass
class Transaction:
    date: str
    value_date: str

    narration: str
    reference: str

    amount: float = 0.0
    transaction_type: str = "UNKNOWN"

    debit: float = 0.0
    credit: float = 0.0

    balance: float = 0.0

    category: str = "Uncategorized"