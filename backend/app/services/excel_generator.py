from openpyxl import Workbook


class ExcelExporter:

    @staticmethod
    def export(transactions, output_path):

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Transactions"

        sheet.append([
            "Date",
            "Value Date",
            "Narration",
            "Reference",
            "Debit",
            "Credit",
            "Balance",
            "Category"
        ])

        for t in transactions:

            sheet.append([
                t.date,
                t.value_date,
                t.narration,
                t.reference,
                t.debit,
                t.credit,
                t.balance,
                t.category
            ])

        workbook.save(output_path)