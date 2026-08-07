import fitz



class PDFReader:

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extracts text from every page of the PDF.
        """

        doc = fitz.open(pdf_path)

        if doc.needs_pass:
            ok = doc.authenticate(password)

            if not ok:
                raise ValueError("Invalid PDF password")

        text = []

        for page in doc:
            page_text = page.get_text()

            if page_text:
                text.append(page_text)

        doc.close()

        return "\n".join(text)