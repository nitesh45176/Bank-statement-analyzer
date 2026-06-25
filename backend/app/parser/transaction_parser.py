import re
from app.services.categorizer import TransactionCategorizer
from app.models.transaction import Transaction

class TransactionParser:

    DATE_PATTERN = re.compile(r"^\d{2}/\d{2}/\d{2}$")

    @classmethod
    def group_transaction_rows(cls, rows):

        grouped = []
        current = None

        STOP_WORDS = [
            "PageNo.",
            "Statementofaccount",
            "AccountBranch",
            "StatementFrom",
            "Nomination",
            "HDFCBANKLIMITED",
            "RegisteredOfficeAddress",
        ]

        for row in rows:

            # Skip empty rows
            if not row:
                continue

            # print("=" * 80)
            # print([word["text"] for word in row])
            # print("=" * 80)

            # Convert the whole row into a single string
            row_text = " ".join(
                word["text"]
                for word in row
            )

            # Remove spaces for easier matching
            cleaned_text = row_text.replace(" ", "")

            # Skip page headers/footers
            if any(stop in cleaned_text for stop in STOP_WORDS):
                continue

            first = row[0]["text"]

            # Skip table header
            if first == "Date":
                continue

            # Start a new transaction
            if cls.DATE_PATTERN.match(first):

                if current is not None:
                    grouped.append(current)

                current = [row]
            
            

            # Continuation line
            else:

                if current is None:
                    continue

                row_text = " ".join(
                    word["text"]
                    for word in row
                ).replace(" ", "").upper()

                IGNORE_ROWS = [
                    "*CLOSINGBALANCE",
                    "CONTENTSOFTHISSTATEMENT",
                    "THISSTATEMENT.",
                    "STATEACCOUNTBRANCHGSTN",
                    "HDFCBANKGSTIN",
                    "REGISTEREDOFFICEADDRESS",
                    "STATEMENTSUMMARY",
                    "OPENINGBALANCE",
                    "GENERATEDON",
                    "THISISACOMPUTERGENERATEDSTATEMENT",

                    # New page header
                    "ACCOUNTBRANCH",
                    "ADDRESS",
                    "CITY",
                    "STATE",
                    "EMAIL",
                    "CUSTID",
                    "ACCOUNTNO",
                    "ACCOUNTSTATUS",
                    "JOINTHOLDERS",
                    "BRANCHCODE",
                    "ACCOUNTTYPE",
                    "NOMINATION",
                    "STATEMENTFROM"
                ]

                row_text = (
                    "".join(word["text"] for word in row)
                    .replace(" ", "")
                    .upper()
                )

                if any(
                    row_text.startswith(prefix)
                    for prefix in IGNORE_ROWS
                ):
                    continue

                current.append(row)

        if current is not None:
            grouped.append(current)

        return grouped
    

    @staticmethod
    def parse_amount(value: str) -> float:

        if not value:
            return 0.0

        return float(
            value.replace(",", "")
        )
    

    @classmethod
    def parse_transaction(cls, grouped_rows):

        first_row = grouped_rows[0]

        texts = [
            word["text"]
            for word in first_row
        ]

        narration_lines = []

        # First line narration
        if len(texts) > 1:
            narration_lines.append(texts[1])

        # Remaining lines
        for row in grouped_rows[1:]:

            narration_lines.append(
                " ".join(
                    word["text"]
                    for word in row
                )
            )

        narration = "\n".join(narration_lines)

        

        date = texts[0]

        balance = cls.parse_amount(texts[-1])

        amount = cls.parse_amount(texts[-2])

        value_date = texts[-3]

        reference = texts[-4]

        narration = " ".join(texts[1:-4])

        # Append continuation rows
        for row in grouped_rows[1:]:
            narration += "\n" + " ".join(
                word["text"]
                for word in row
            )

        transaction_type = cls.detect_transaction_type(narration)

        transaction = Transaction(
            date=date,
            value_date=value_date,
            narration=narration,
            reference=reference,
            amount=amount,
            transaction_type=transaction_type,
            balance=balance
        )

        if transaction_type == "DEBIT":
            transaction.debit = amount

        elif transaction_type == "CREDIT":
            transaction.credit = amount

        transaction.category = TransactionCategorizer.categorize(
        transaction.narration
)

        return transaction
    

    @staticmethod
    def detect_transaction_type(narration: str) -> str:

        narration = narration.upper()

        credit_keywords = [
    "RTGSCR",
    "NEFTCR",
    "IMPS CR",
    "FT-CR",
    "RTGS CR",
    "NEFT CR",
    "CREDIT",
    "SALARY",
]

        debit_keywords = [
    "RTGSDR",
    "NEFTDR",
    "IMPS DR",
    "FT-DR",
    "GST/BANK",
    "ACH",
    "AUTOPAY",
    "ATM",
    "POS",
    "CHARGES",
]

        

        for keyword in credit_keywords:
            if keyword in narration:
                return "CREDIT"

        for keyword in debit_keywords:
            if keyword in narration:
                return "DEBIT"

        return "UNKNOWN"
    

    @classmethod
    def build_transactions(cls, grouped_rows):

        transactions = []

        for transaction_rows in grouped_rows:

            transaction = cls.parse_transaction(
                transaction_rows
            )

            transactions.append(transaction)

        return transactions