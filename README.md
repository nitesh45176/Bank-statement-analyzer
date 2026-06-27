# 📄 Bank Statement Analyzer

A full-stack web application that analyzes **HDFC Bank PDF statements**, extracts every transaction, categorizes them using rule-based keyword matching, generates insightful analytics, and exports the results as a **3-sheet Excel report**.

Built as part of the **Correm Advisory – Full Stack Engineer Hiring Assignment**.

---

## 🚀 Live Demo

### Frontend

🔗 https://bank-statement-analyzer-sandy.vercel.app/

### Backend API

🔗 https://bank-statement-analyzer-x2z0.onrender.com

### API Documentation

🔗 https://bank-statement-analyzer-x2z0.onrender.com/docs

---

# ✨ Features

### 📄 PDF Processing

* Upload HDFC Bank PDF statements
* Extract transactions using **PyMuPDF**
* Handles multi-line transaction descriptions
* Parses account details
* Maintains Transaction order
* Zero dropped transactions (for supported statement format)

---

### 💳 Transaction Parsing

Extracts:

* Date
* Value Date
* Narration
* Reference Number
* Debit Amount
* Credit Amount
* Running Balance

Automatically determines whether a transaction is:

* Credit
* Debit

---

### 🏷 Smart Categorization

Transactions are categorized using keyword-based matching.

Supported categories include:

* Salary
* EMI / Loan
* Food & Dining
* Shopping
* Travel
* Utilities
* Telecom
* Entertainment
* Healthcare
* Education
* Investments
* Insurance
* Cash Withdrawal
* UPI / Bank Transfer
* Rent
* Tax
* Uncategorized

---

### 📊 Analytics

The application generates:

* Total Transactions
* Total Credits
* Total Debits
* Closing Balance
* Highest Credit
* Highest Debit

Monthly analytics:

* Credit per month
* Debit per month
* Transaction count

Additional insights:

* Top 5 Credits
* Top 5 Debits
* Category Summary
* Salary Detection
* EMI Detection
* Categorized Percentage

---

### 📑 Excel Export

Generates a downloadable Excel workbook containing **3 sheets**.

### Sheet 1 — Account Details

* Account Holder
* Account Number
* Bank Name
* Branch
* IFSC
* Statement Period
* Opening Balance
* Closing Balance

---

### Sheet 2 — Transaction Ledger

Contains every transaction with:

* Date
* Value Date
* Narration
* Reference
* Debit
* Credit
* Balance
* Category

---

### Sheet 3 — Analytics

Contains:

* Category Summary
* Monthly Summary
* Total Credits
* Total Debits
* Transaction Statistics

---

# 🏗 Architecture

```
React Frontend
        │
        │ Upload PDF
        ▼
FastAPI Backend
        │
        ├── PDF Reader (PyMuPDF)
        │
        ├── Word Parser
        │
        ├── Transaction Parser
        │
        ├── Categorization Engine
        │
        ├── Analytics Engine
        │
        └── Excel Generator
                │
                ▼
         Download Excel Report
```

---

# 🛠 Tech Stack

## Frontend

* React
* Axios
* Tailwind CSS
* Vite

## Backend

* FastAPI
* Python 3.10+
* PyMuPDF
* OpenPyXL
* Uvicorn

---

# 📂 Project Structure

```
backend/
│
├── app/
│   ├── api/
│   ├── parser/
│   ├── services/
│   ├── models/
│   ├── uploads/
│   └── main.py
│
├── requirements.txt
│
└── ...

frontend/
│
├── src/
│   ├── api/
│   ├── components/
│   ├── pages/
│   └── ...
│
└── package.json
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository-url>
cd bank-statement-analyzer
```

---

## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# API Endpoints

## Upload Statement

```
POST /upload
```

Accepts:

* multipart/form-data
* PDF file

Returns:

* Account Details
* Analytics
* Monthly Summary
* Category Summary
* Salary Detection
* EMI Detection
* Top Credits
* Top Debits
* Excel file location

---

## Download Excel

```
GET /download
```

Downloads the generated Excel workbook.

---

# Assumptions

* Designed for HDFC Bank statement format used in the assignment.
* Categorization is keyword/rule-based.
* OCR for scanned PDFs is not implemented.
* Excel file is generated on demand.
* Deployment uses Render (backend) and Vercel (frontend).

---

# AI Tools Used

The following AI tools were used during development:

* ChatGPT (OpenAI)

Used for:

* Architecture planning
* FastAPI implementation guidance
* React component structuring
* Debugging assistance
* Regex refinement
* Excel generation logic
* Deployment guidance
* Code review and optimization

All generated code was reviewed, integrated, tested, and modified manually before submission.

---

# Future Improvements

* OCR support for scanned PDFs
* Database integration
* User authentication
* Transaction search and filtering
* Charts and dashboards
* Improved categorization using configurable rules
* Persistent upload history
* Multi-bank support

---

# Author

**Nitesh Kumar Mishra**

Full Stack Developer | Python | FastAPI | React | MERN

GitHub: https://github.com/nitesh45176

---

## 📌 Assignment

Correm Advisory — Full Stack Engineer Hiring Assignment

**Thank you for reviewing this project!**
