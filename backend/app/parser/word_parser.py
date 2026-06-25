import pdfplumber
from collections import defaultdict


class WordParser:

    ROW_TOLERANCE = 3

    @staticmethod
    def extract_words(pdf_path: str):

        words = []

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_words = page.extract_words(
                    x_tolerance=2,
                    y_tolerance=2,
                    keep_blank_chars=False
                )

                words.extend(page_words)

        return words

    @classmethod
    def group_rows(cls, words):

        rows = []

        for word in sorted(words, key=lambda w: w["doctop"]):

            if not rows:
                rows.append([word])
                continue

            last_row = rows[-1]

            if abs(word["doctop"] - last_row[0]["doctop"]) <= cls.ROW_TOLERANCE:
                last_row.append(word)
            else:
                rows.append([word])

        for row in rows:
            row.sort(key=lambda w: w["x0"])

        return rows