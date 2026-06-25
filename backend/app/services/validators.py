class StatementValidator:

    @staticmethod
    def validate(transactions):

        valid = True

        for i in range(1, len(transactions)):

            prev = transactions[i-1]
            curr = transactions[i]

            expected = prev.balance + curr.credit - curr.debit

            if abs(expected - curr.balance) > 1:
                valid = False
                break

        return valid