import re

from app.models.transaction import Transaction
from app.parser.common_parser import CommonParser
from app.parser.pnb.account_parser import PNBAccountParser
from app.services.categorizer import TransactionCategorizer


class PNBParser(CommonParser):

    DATE_PATTERN = re.compile(
    r"^\d{2}[-/](?:\d{2}|[A-Za-z]{3})[-/](?:\d{2}|\d{4})$"
)

    def parse_account_details(self, text):
        return PNBAccountParser.parse(text)

    @classmethod
    def group_transaction_rows(cls, rows):

        grouped = []
        current = None

        for row in rows:

            if not row:
                continue

            first = row[0]["text"].strip()

            print(repr(first))

            if cls.DATE_PATTERN.match(first):

                if current:
                    grouped.append(current)

                current = [row]

            else:

                row_text = " ".join(
                    word["text"] for word in row
                ).upper()

                STOP_WORDS = [
                    "CLOSING BALANCE",
                    "LOAN SUMMARY",
                    "TOTAL RELATIONSHIP VALUE",
                    "DOWNLOAD",
                    "VIGILANCE",
                    "PNB ONE APP",
                    "ACCOUNT NUMBER",
                ]

                if any(word in row_text for word in STOP_WORDS):
                    continue

                if current:
                    current.append(row)

        if current:
            grouped.append(current)


        return grouped

    

    @classmethod
    def parse_transaction(cls, grouped_rows):

        first_row = grouped_rows[0]

        texts = [
            word["text"].strip()
            for word in first_row
        ]
        
        print(texts)


        date = texts[0]

        balance = texts[-1]

        amount = texts[-2]

        narration = " ".join(texts[1:-2])

        reference = ""

        balance = cls.clean_amount(balance)
        amount = cls.clean_amount(amount)



        upper = narration.upper()

        if "/CR/" in upper:
            transaction_type = "CREDIT"
        elif "/DR/" in upper:
            transaction_type = "DEBIT"
        else:
            transaction_type = "UNKNOWN"


        for row in grouped_rows[1:]:

            narration += "\n"

            narration += " ".join(
                word["text"]
                for word in row
            )

        transaction = Transaction(
    date=date,
    value_date=date,
    narration=narration,
    reference="",
    amount=amount,
    balance=balance,
    transaction_type=transaction_type,
)

        transaction.category = TransactionCategorizer.categorize(
            narration
        )

        if transaction_type == "CREDIT":
            transaction.credit = amount
        else:
            transaction.debit = amount

        print("=" * 80)
        print("DATE:", transaction.date)
        print("NARRATION:", transaction.narration)
        print("AMOUNT:", transaction.amount)
        print("CREDIT:", transaction.credit)
        print("DEBIT:", transaction.debit)
        print("BALANCE:", transaction.balance)
        print("TYPE:", transaction.transaction_type)

        return transaction

    @staticmethod
    def clean_amount(value):

        if not value:
            return 0.0

        value = (
            value.replace(",", "")
                .replace("CR.", "")
                .replace("DR.", "")
                .strip()
        )

        return float(value) if value else 0.0


    


    def parse_transactions(self, grouped_rows):
         return self.build_transactions(grouped_rows)

        


    def parse_transactions_from_ocr(self, text):

        transactions = []

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        date_pattern = re.compile(r"\d{2}-[A-Za-z]{3}-\d{4}")

        # -------------------------
        # Locate SAVINGS account table
        # -------------------------
        start = None

        for i, line in enumerate(lines):

            if "SAVINGSFUNDGENERAL" in line.upper():

                for j in range(i, min(i + 20, len(lines))):

                    if (
                        lines[j] == "Date"
                        and j + 1 < len(lines)
                        and lines[j + 1] == "Particulars"
                    ):
                        start = j + 8
                        break

                break

        if start is None:
            print("Savings table not found.")
            return []


        i = start

        while i < len(lines):

            if "Closing Balance" in lines[i]:
                break

            if not date_pattern.fullmatch(lines[i]):
                i += 1
                continue

            date = lines[i]
            i += 1

            block = []

            while i < len(lines):

                if "Closing Balance" in lines[i]:
                    break

                if date_pattern.fullmatch(lines[i]):
                    break

                block.append(lines[i])
                i += 1

            if len(block) < 2:
                continue

            balance_str = block[-1]
            amount_str = block[-2]
            narration = " ".join(block[:-2])

            try:
                amount = float(amount_str.replace(",", ""))
            except:
                amount = 0.0

            balance = float(
                balance_str
                .replace("CR.", "")
                .replace("DR.", "")
                .replace(",", "")
            )

            narration_upper = narration.upper()

            credit = 0.0
            debit = 0.0
            transaction_type = "UNKNOWN"

            if "/CR/" in narration_upper or "INT.PD" in narration_upper:
                credit = amount
                transaction_type = "CREDIT"

            elif "/DR/" in narration_upper:
                debit = amount
                transaction_type = "DEBIT"

            transactions.append(
                Transaction(
                    date=date,
                    value_date=date,
                    narration=narration,
                    reference="",
                    amount=amount,
                    transaction_type=transaction_type,
                    debit=debit,
                    credit=credit,
                    balance=balance,
                    category="Uncategorized",
                )
            )

        print(f"OCR Transactions Parsed: {len(transactions)}")

        for t in transactions:
            print(
                t.date,
                t.credit,
                t.debit,
                t.balance,
                t.narration
            )

        return transactions