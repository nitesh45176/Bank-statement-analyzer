from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base


class StatementModel(Base):
    __tablename__ = "statements"

    statement_id = Column(String, primary_key=True, index=True)
    bank = Column(String, nullable=True)
    account_details = Column(Text, nullable=True)  # JSON string
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = relationship(
        "TransactionModel",
        back_populates="statement",
        cascade="all, delete-orphan",
    )


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)  # statement_id + index
    statement_id = Column(String, ForeignKey("statements.statement_id"), index=True)

    date = Column(String, nullable=True)
    value_date = Column(String, nullable=True)
    narration = Column(Text, nullable=True)
    reference = Column(String, nullable=True)
    amount = Column(Float, default=0.0)
    transaction_type = Column(String, default="UNKNOWN")
    debit = Column(Float, default=0.0)
    credit = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)
    category = Column(String, default="Uncategorized")

    statement = relationship("StatementModel", back_populates="transactions")
