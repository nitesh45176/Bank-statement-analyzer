import fitz


class PDFReader:

    @staticmethod
    def extract_text(pdf_path: str, password: str = "") -> str:
        """
        Extract text from every page of the PDF.
        Supports password-protected PDFs when a password is provided.
        """

        doc = fitz.open(pdf_path)

        if doc.needs_pass:
            if not password:
                doc.close()
                raise ValueError("PDF is password protected")

            if not doc.authenticate(password):
                doc.close()
                raise ValueError("Invalid PDF password")

        text = []

        for page in doc:
            page_text = page.get_text()

            if page_text:
                text.append(page_text)

        doc.close()

        return "\n".join(text)