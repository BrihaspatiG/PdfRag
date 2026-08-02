import os
import fitz
from app.services.text_cleaner import TextCleaner


class PDFParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.document = None
        self.cleaner = TextCleaner()

    def open_pdf(self):
        self.document = fitz.open(self.pdf_path)

    def get_page_count(self):
        return len(self.document)

    def close_pdf(self):
        if self.document is not None:
            self.document.close()
            self.document = None

    def extract_text(self):
        extracted_pages = []
        for page_number in range(len(self.document)):
            page = self.document[page_number]
            text = page.get_text()
            text = self.cleaner.clean(text)
            page_data = {
                "filename": os.path.basename(self.pdf_path),
                "page": page_number + 1,
                "text": text,
                "ocr_required": len(text) == 0
            }
            extracted_pages.append(page_data)
        return extracted_pages