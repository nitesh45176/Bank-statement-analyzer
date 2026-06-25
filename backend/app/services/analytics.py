from app.models.transaction import Transaction
from datetime import datetime
from collections import defaultdict

class AnalyticsService:

    @staticmethod
    def generate_summary(transactions: list[Transaction]):

        total_transactions = len(transactions)

        total_credit = sum(
            t.credit
            for t in transactions
        )

        total_debit = sum(
            t.debit
            for t in transactions
        )

        closing_balance = (
            transactions[-1].balance
            if transactions
            else 0
        )

        highest_credit = max(
            (t.credit for t in transactions),
            default=0
        )

        highest_debit = max(
            (t.debit for t in transactions),
            default=0
        )

        return {
            "total_transactions": total_transactions,
            "total_credit": total_credit,
            "total_debit": total_debit,
            "closing_balance": closing_balance,
            "highest_credit": highest_credit,
            "highest_debit": highest_debit
        }


    @staticmethod
    def monthly_summary(transactions):

        monthly = defaultdict(
            lambda: {
                "credit": 0,
                "debit": 0,
                "count": 0
            }
        )

        for t in transactions:

            month = datetime.strptime(
    t.date,
    "%d/%m/%y"
).strftime("%b %Y")

            monthly[month]["credit"] += t.credit
            monthly[month]["debit"] += t.debit
            monthly[month]["count"] += 1

        return monthly

    @staticmethod
    def top_credits(transactions):

        return sorted(
            transactions,
            key=lambda t: t.credit,
            reverse=True
        )[:5]

    
    @staticmethod
    def top_debits(transactions):

        return sorted(
            transactions,
            key=lambda t: t.debit,
            reverse=True
        )[:5]