import re


class AccountParser:

    @staticmethod
    def parse(text: str):

        details = {}

        # Account Holder
        holder = re.search(
            r"Statement of account\s+M/S\.\s+(.*?)\s+C/O",
            text,
            re.DOTALL | re.IGNORECASE
        )

        details["account_holder"] = (
            "M/S. " + holder.group(1).strip()
            if holder else ""
        )

        # Account Number
        account = re.search(
            r"Account No\s*:\s*(\d+)",
            text
        )

        details["account_number"] = (
            account.group(1)
            if account else ""
        )

        # Branch
        branch = re.search(
            r"Account Branch\s*:\s*(.*)",
            text
        )

        details["branch"] = (
            branch.group(1).strip()
            if branch else ""
        )

        # IFSC
        ifsc = re.search(
            r"RTGS/NEFT IFSC\s*:\s*([A-Z0-9]+)",
            text
        )

        details["ifsc"] = (
            ifsc.group(1)
            if ifsc else ""
        )

        # Statement Period
        period = re.search(
            r"Statement From\s*:\s*(.*?)\s*To\s*:\s*(.*)",
            text
        )

        if period:
            details["statement_from"] = period.group(1).strip()
            details["statement_to"] = period.group(2).strip()
        else:
            details["statement_from"] = ""
            details["statement_to"] = ""
        
        # Statement Summary
        summary = re.search(
            r"STATEMENT SUMMARY :-\s*"
            r"Opening Balance\s*"
            r"Dr Count\s*"
            r"Cr Count\s*"
            r"Debits\s*"
            r"Credits\s*"
            r"Closing Bal\s*"
            r"(-?[\d,]+\.\d+)\s*"
            r"(\d+)\s*"
            r"(\d+)\s*"
            r"([\d,]+\.\d+)\s*"
            r"([\d,]+\.\d+)\s*"
            r"(-?[\d,]+\.\d+)",
            text,
            re.DOTALL | re.IGNORECASE
        )

        if summary:

            details["opening_balance"] = float(
                summary.group(1).replace(",", "")
            )

            details["debit_count"] = int(summary.group(2))

            details["credit_count"] = int(summary.group(3))

            details["total_debit"] = float(
                summary.group(4).replace(",", "")
            )

            details["total_credit"] = float(
                summary.group(5).replace(",", "")
            )

            details["closing_balance"] = float(
                summary.group(6).replace(",", "")
            )

        else:

            details["opening_balance"] = ""
            details["debit_count"] = 0
            details["credit_count"] = 0
            details["total_debit"] = 0
            details["total_credit"] = 0
            details["closing_balance"] = 0
        details["bank_name"] = "HDFC Bank"

        return details