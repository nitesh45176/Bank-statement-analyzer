import fitz



class PDFReader:

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extracts text from every page of the PDF.
        """

        document = fitz.open(pdf_path)

        text = []

        for page in document:
            page_text = page.get_text()

            if page_text:
                text.append(page_text)

        document.close()

        return "\n".join(text)