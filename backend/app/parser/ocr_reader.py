import fitz
import numpy as np

from rapidocr_onnxruntime import RapidOCR


class OCRReader:

    ocr = RapidOCR()

    @staticmethod
    def extract_text(pdf_path):

        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:

            pix = page.get_pixmap(dpi=300)

            img = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            ).reshape(
                pix.height,
                pix.width,
                pix.n
            )

            result, _ = OCRReader.ocr(img)

            if result:

                for line in result:
                    text += line[1] + "\n"

        return text