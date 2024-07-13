"""
PDF generator script
"""

import json
from datetime import datetime
import logging
from typing import List
from fpdf import FPDF
from .doc_printing import Document
from .fonts.fonts import Fonts
import base64
from io import BytesIO

TEXT_FOLDER = "src/form_text"
SIGNATURE_FOLDER = "src/signatures"
LOGO_FOLDER = "src/logo"
LOGO_FILE = f"{LOGO_FOLDER}/logo.png"


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class GeneratePDF:
    """Class used to generate a consent form PDF"""

    def __init__(self):
        self.pdf = FPDF()
        try:
            self.fonts = Fonts()
        except (RuntimeError, FileNotFoundError, json.JSONDecodeError) as e:
            logging.error("PDF generator cannot be made: %s", e)
            
    def add_base64_image(self, base64_data: str, h=None):
        if "base64," in base64_data:
            base64_data = base64_data.split("base64,")[1]
        
        image_data = base64.b64decode(base64_data)
        image_file = BytesIO(image_data)
        self.pdf.image(image_file, h=h)

    def generate_pdf(self, token: str, client_name: str, form_name: str,
                     consent_flags: List[bool], siganture_base64: str) -> None:
        """Generates a PDF document with the specified token, client name, and form name"""
        self.pdf.add_page()

        try:
            # Add logo
            self.pdf.image(LOGO_FILE, w=25, x=15, y=11)

            # Print document text
            form_dict = self._get_json_dict(form_name)
            document: Document = Document(self.pdf, self.fonts, consent_flags, form_dict["document"])
            document.print()

            # Space
            self.pdf.cell(0, 5, text = "", ln = True)

            # Add signature
            self.add_base64_image(siganture_base64, h = 20)

            # Space
            self.pdf.cell(0, 5, text = "", ln = True)

            # Add client's name
            self.pdf.cell(0, 5, text = client_name, ln = True, align = "L")

            # Add date
            date: str = datetime.now().strftime("%d %B %Y")
            self.pdf.cell(0, 5, text = date, ln = True, align = "L")
 
            #pdf_path = f"/app/pdfs/{token}.pdf"  # Path where PDF will be saved
            pdf_path = f"{token}.pdf"

            self.pdf.output(name=pdf_path)
            logging.info("%s.pdf successfully generated", token)

        except Exception as e:
            logging.error("PDF generation failed: %s %s", e, type(e))
            raise


    def _get_json_dict(self, form_name: str):
        try:
            with open(f"{TEXT_FOLDER}/{form_name}.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error("Cannot read {form_name} config file: %s", e)
            raise

# def main():
    # """Testing"""
    # generator = GeneratePDF()
    # generator.generate_pdf("test1", "Gerald", "adult", [True, False, True])


# if __name__ == "__main__":
#     main()
