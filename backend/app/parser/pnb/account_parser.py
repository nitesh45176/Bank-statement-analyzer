import re


class PNBAccountParser:

    @staticmethod
    def extract(pattern, text):
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

        return ""


    @classmethod
    def parse(cls, text):

        return {
            "account_holder": cls.extract(
                r"Customer Name\s*:?(.+)",
                text
            ),

            "account_number": cls.extract(
                r"Account Number\s+(\d+)",
                text
            ),

            "branch": cls.extract(
                r"Name\s*:([^\n]+)",
                text
            ),

            "ifsc": cls.extract(
                r"IFSC\s*:?\s*([A-Z0-9]+)",
                text
            ),

            "statement_period": cls.extract(
                r"Statement Period\s*:?\s*(.+)",
                text
            ),
        }