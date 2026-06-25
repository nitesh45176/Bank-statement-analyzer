class TransactionCategorizer:

    CATEGORY_RULES = {

        "Salary": [
            "SALARY"
        ],

        "Bank Transfer": [
            "RTGS",
            "NEFT",
            "IMPS",
            "FT-CR",
            "TRANSFER",
            "A2A"
        ],

        "UPI": [
            "UPI"
        ],

        "Tax": [
            "GST"
        ],

        "Bank Charges": [
            "CHARGES",
            "PENAL"
        ],

        "Loan": [
            "LOAN",
            "FINANCE",
            "CAPITAL"
        ],

        "Rent": [
            "RENT"
        ],

        "Cash Withdrawal": [
            "ATM"
        ],

        "Shopping": [
            "POS"
        ],

        "Interest": [
            "INTEREST"
        ]
    }

    @classmethod
    def categorize(cls, narration: str):

        narration = narration.upper()

        for category, keywords in cls.CATEGORY_RULES.items():

            for keyword in keywords:

                if keyword in narration:
                    return category

        return "Uncategorized"