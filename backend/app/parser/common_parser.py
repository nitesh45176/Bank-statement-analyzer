from app.parser.base_parser import BaseParser


class CommonParser(BaseParser):



    @staticmethod
    def parse_amount(value: str) -> float:

        if not value:
            return 0.0

        return float(
            value.replace(",", "")
        )

    @classmethod
    def build_transactions(cls, grouped_rows):

        transactions = []

        for transaction_rows in grouped_rows:

            transaction = cls.parse_transaction(
                transaction_rows
            )

            transactions.append(transaction)

        return transactions

    def parse_transactions(self, grouped_rows):
        return self.build_transactions(grouped_rows)