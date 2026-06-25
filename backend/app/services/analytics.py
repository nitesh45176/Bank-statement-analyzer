from app.models.transaction import Transaction
from datetime import datetime
from collections import defaultdict

class AnalyticsService:

    @staticmethod
    def generate_summary(transactions: list[Transaction]):

        total_transactions = len(transactions)

        total_credit = sum(t.credit for t in transactions)
        total_debit = sum(t.debit for t in transactions)

        credit_count = sum(
            1 for t in transactions
            if t.credit > 0
        )

        debit_count = sum(
            1 for t in transactions
            if t.debit > 0
        )

        closing_balance = (
            transactions[-1].balance
            if transactions else 0
        )

        highest_credit = max(
            (t.credit for t in transactions),
            default=0
        )

        highest_debit = max(
            (t.debit for t in transactions),
            default=0
        )

        categorized = sum(
            1
            for t in transactions
            if t.category != "Uncategorized"
        )

        uncategorized = total_transactions - categorized

        return {
            "total_transactions": total_transactions,

            "credit_count": credit_count,
            "debit_count": debit_count,

            "total_credit": total_credit,
            "total_debit": total_debit,

            "closing_balance": closing_balance,

            "highest_credit": highest_credit,
            "highest_debit": highest_debit,

            "categorized_percent":
                round(categorized * 100 / total_transactions, 2),

            "uncategorized_percent":
                round(uncategorized * 100 / total_transactions, 2)
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
    

    @staticmethod
    def category_summary(transactions):

        summary = defaultdict(
            lambda: {
                "credit": 0,
                "debit": 0,
                "count": 0
            }
        )

        for t in transactions:

            summary[t.category]["credit"] += t.credit
            summary[t.category]["debit"] += t.debit
            summary[t.category]["count"] += 1

        return dict(summary)
    

    @staticmethod
    def categorized_percentage(transactions):

        total = len(transactions)

        categorized = sum(
            1
            for t in transactions
            if t.category != "Uncategorized"
        )

        return {
            "categorized": round(
                categorized * 100 / total,
                2
            ),
            "uncategorized": round(
                (total - categorized) * 100 / total,
                2
            )
        }
    

    @staticmethod
    def category_summary(transactions):

        summary = {}

        for t in transactions:

            if t.category not in summary:

                summary[t.category] = {
                    "debit": 0,
                    "credit": 0,
                    "count": 0
                }

            summary[t.category]["debit"] += t.debit
            summary[t.category]["credit"] += t.credit
            summary[t.category]["count"] += 1

        return summary
    

    @staticmethod
    def salary_detection(transactions):

        salary_map = defaultdict(list)

        salary_keywords = [
            "SALARY",
            "SAL",
            "PAYROLL",
            "WAGES",
            "STIPEND"
        ]

        for t in transactions:

            narration = t.narration.upper()

            if t.credit <= 0:
                continue

            if any(keyword in narration for keyword in salary_keywords):

                key = round(t.credit, -2)

                salary_map[key].append(t)

        detected = []

        for amount, txns in salary_map.items():

            if len(txns) >= 2:

                detected.append({
                    "amount": amount,
                    "months": len(txns),
                    "latest_reference": txns[-1].reference
                })

        return detected
    

    @staticmethod
    def emi_detection(transactions):

        emi_map = defaultdict(list)

        emi_keywords = [
            "EMI",
            "LOAN",
            "ACH D",
            "ECS",
            "NACH",
            "BAJAJ",
            "ADITYA",
            "TATA",
            "UGRO",
            "CAPITAL",
            "FEDBANK"
        ]

        for t in transactions:

            if t.debit <= 0:
                continue

            narration = t.narration.upper()

            if any(keyword in narration for keyword in emi_keywords):

                key = round(t.debit, -1)

                emi_map[key].append(t)

        detected = []

        for amount, txns in emi_map.items():

            if len(txns) >= 2:

                detected.append({
                    "amount": amount,
                    "occurrences": len(txns),
                    "latest_reference": txns[-1].reference
                })

        return detected