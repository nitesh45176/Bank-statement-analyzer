class BankDetector:

    BANK_SIGNATURES = {
        "HDFC": [
            "HDFC BANK",
            "HDFC BANK LIMITED",
        ],

        "PNB": [
            "PNB ONE",
            "CARE@PNB.CO.IN",
            "DEPOSIT ACCOUNT SUMMARY",
            "LOAN SUMMARY",
            "CUST ID",
            "BRANCH ID",
        ],
    }

    @classmethod
    def detect(cls, text: str):

        text = text.upper()

        for bank, signatures in cls.BANK_SIGNATURES.items():
            for signature in signatures:
                if signature.upper() in text:
                    print(f"Detected: {bank} (matched '{signature}')")
                    return bank

        return "UNKNOWN"