from fastapi import APIRouter, UploadFile, File
import os
from app.parser.transaction_parser import TransactionParser
from app.parser.pdf_reader import PDFReader
from app.parser.word_parser import WordParser
from app.services.excel_generator import ExcelExporter
from app.services.analytics import AnalyticsService
from app.parser.account_parser import AccountParser
from fastapi.responses import FileResponse


router = APIRouter()

UPLOAD_DIR = "app/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as pdf:

        pdf.write(
            await file.read()
        )

    extracted_text = PDFReader.extract_text(file_path)

    with open("debug.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
    # print(extracted_text[:5000])
    account_details = AccountParser.parse(extracted_text)
    # lines = TransactionParser.preprocess(extracted_text)

    # blocks = TransactionParser.group_transactions(lines)


    words = WordParser.extract_words(file_path)
    rows = WordParser.group_rows(words)

    # transactions = TransactionParser.build_transactions(rows)



    grouped = TransactionParser.group_transaction_rows(rows)

    transactions = TransactionParser.build_transactions(grouped)


    summary = AnalyticsService.generate_summary(transactions)
    monthly_summary = AnalyticsService.monthly_summary(transactions)
    category_summary = AnalyticsService.category_summary(transactions)
    top_credits = AnalyticsService.top_credits(transactions)
    top_debits = AnalyticsService.top_debits(transactions)

    
    
    output_file = "app/uploads/transactions.xlsx"


    

    category_summary = AnalyticsService.category_summary(transactions)
    salary_detection = AnalyticsService.salary_detection(transactions)
    emi_detection = AnalyticsService.emi_detection(transactions)
    categorized_percentage = AnalyticsService.categorized_percentage(transactions)

    output_file = "app/uploads/transactions.xlsx"

    ExcelExporter.export(
    account_details,
    transactions,
    summary,
    monthly_summary,
    category_summary,
    
    output_file
)

    category_summary = AnalyticsService.category_summary(transactions)

    categorized_percentage = AnalyticsService.categorized_percentage(transactions)
    
    return {
    "summary": summary,
    "account_details": account_details,
    "monthly_summary": monthly_summary,
    "category_summary": category_summary,
    "salary_detection": salary_detection,
    "emi_detection": emi_detection,
    "balance_chain_valid": True,
    "top_credits": top_credits,
    "top_debits": top_debits,
    "category_summary": category_summary,
    "categorized_percentage": categorized_percentage,
    "excel_file": output_file
}



@router.get("/download")
def download_excel():
    return FileResponse(
        "app/uploads/transactions.xlsx",
        filename="transactions.xlsx"
    )