from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import os

from app.parser.pdf_reader import PDFReader
from app.parser.word_parser import WordParser
from app.parser.detector import BankDetector
from app.parser.factory import ParserFactory
from app.parser.ocr_reader import OCRReader
from app.services.analytics import AnalyticsService
from app.services.excel_generator import ExcelExporter
import uuid

from app.services.statement_store import StatementStore
from app.rag.ingest import ingest_transactions

router = APIRouter()

UPLOAD_DIR = os.path.join(os.getcwd(), "data", "uploads")
OUTPUT_FILE = os.path.join(UPLOAD_DIR, "transactions.xlsx")

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):

    # Save uploaded PDF
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as pdf:
        pdf.write(await file.read())

    # Read PDF
    print("1. PDFReader")
    extracted_text = PDFReader.extract_text(file_path)  
    print(extracted_text[:3000])  


    print("2. WordParser")
    words = WordParser.extract_words(file_path)
    print("Words:", len(words))


    # -----------------------------
    # Normal PDF
    # -----------------------------
    if words:

        print("Normal PDF detected.")

        bank = BankDetector.detect(extracted_text)
        print("Detected Bank:", bank)

        parser = ParserFactory.get_parser(bank)

        account_details = parser.parse_account_details(extracted_text)

        rows = WordParser.group_rows(words)
        grouped_rows = parser.group_transaction_rows(rows)
        transactions = parser.parse_transactions(grouped_rows)
        print("Transactions:", len(transactions))



    # -----------------------------
    # Scanned PDF
    # -----------------------------
    else:

        print("Scanned PDF detected.")
        print("Running OCR...")

        extracted_text = OCRReader.extract_text(file_path)

        print(extracted_text[:500])

        bank = BankDetector.detect(extracted_text)
        print("Detected Bank:", bank)

        parser = ParserFactory.get_parser(bank)

        account_details = parser.parse_account_details(extracted_text)

        # Temporary until OCR transaction parser is built
        rows = []
        grouped_rows = []
        transactions = parser.parse_transactions_from_ocr(extracted_text)
        print("\nParsed Transactions\n")

        for t in transactions:
            print(t)
    
    


    # Analytics
    summary = AnalyticsService.generate_summary(transactions)
    monthly_summary = AnalyticsService.monthly_summary(transactions)
    category_summary = AnalyticsService.category_summary(transactions)

    salary_detection = AnalyticsService.salary_detection(transactions)
    emi_detection = AnalyticsService.emi_detection(transactions)

    top_credits = AnalyticsService.top_credits(transactions)
    top_debits = AnalyticsService.top_debits(transactions)

    categorized_percentage = (
        AnalyticsService.categorized_percentage(transactions)
        if transactions
        else {
            "categorized": 0,
            "uncategorized": 0,
        }
    )


    # -----------------------------
    # AI Statement Store + RAG
    # -----------------------------
    statement_id = str(uuid.uuid4())

    StatementStore.save(
        statement_id,
        {
            "transactions": transactions,
            "account_details": account_details,
        },
    )

    # Background RAG ingestion so the upload response returns immediately
    background_tasks.add_task(
        ingest_transactions,
        statement_id,
        transactions,
    )

    print("Statement ID:", statement_id)

    
    # Export Excel
    print("Type of monthly_summary:", type(monthly_summary))
    print("Value of monthly_summary:", monthly_summary)

    print("Type of category_summary:", type(category_summary))
    print("Type of summary:", type(summary))
    ExcelExporter.export(
        account_details,
        transactions,
        summary,
        monthly_summary,
        category_summary,
        OUTPUT_FILE,
    )

    return {
        "statement_id": statement_id,
        "rows": len(rows),
        "grouped_rows": len(grouped_rows),
        "transactions": transactions,
        "detected_bank": bank,
        "account_details": account_details,
        "summary": summary,
        "monthly_summary": monthly_summary,
        "category_summary": category_summary,
        "salary_detection": salary_detection,
        "emi_detection": emi_detection,
        "top_credits": top_credits,
        "top_debits": top_debits,
        "categorized_percentage": categorized_percentage,
        "excel_file": OUTPUT_FILE,
    }


@router.get("/download")
def download_excel():
    if not os.path.exists(OUTPUT_FILE):
        raise HTTPException(
            status_code=404,
            detail="Transactions excel file not found. Please upload a statement first."
        )
    return FileResponse(
        OUTPUT_FILE,
        filename="transactions.xlsx",
    )