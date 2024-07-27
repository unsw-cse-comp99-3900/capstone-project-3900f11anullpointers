"""Module for generating PDFs.

This module is responsible for generating consent form PDFs using the FPDF library. 
It defines the GeneratePDF class, which handles the creation and formatting of 
the PDF documents, including adding logo, signatures, and text content.

Classes:
- GeneratePDF: Handles the generation of a PDF document with consent information, 
  client signatures, and other details.

Constants:
- TEXT_FOLDER: Directory containing form text configuration files.
- LOGO_FOLDER: Directory containing the logo image.
- LOGO_FILE: Path to the logo image file.
"""

import json
import base64
import logging
from datetime import datetime
from typing import Any, Dict, List
from io import BytesIO
from fpdf import FPDF
from .doc_printing import Document
from .fonts.fonts import Fonts

TEXT_FOLDER = "src/form_text"
LOGO_FOLDER = "src/logo"
LOGO_FILE = f"{LOGO_FOLDER}/logo.png"

logging.getLogger('fontTools.subset').level = logging.WARN
logging.getLogger('fontTools.ttLib.ttFont').level = logging.WARN
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

class GeneratePDF:
    """
    Handles the generation of a PDF document with consent information, 
    client signatures, and other details.
    """

    def __init__(self):
        self.pdf = FPDF()
        try:
            self.fonts = Fonts()
        except (RuntimeError, FileNotFoundError, json.JSONDecodeError) as e:
            logging.error("PDF generator cannot be made: %s", e)

    def _add_base64_image(self, base64_data: str, h=None) -> None:
        try:
            if "base64," in base64_data:
                base64_data: str = base64_data.split("base64,")[1]

            image_data: bytes = base64.b64decode(base64_data)
            image_file: BytesIO = BytesIO(image_data)
            self.pdf.image(image_file, h=h)
        except (ValueError, TypeError) as e:
            logging.error("Error addding base64 image: %s", e)

    def generate_pdf(self, client_name: str, form_name: str, consent_flags: List[bool],
                     siganture_base64: str, submit_datetime: datetime) -> str:
        """Generates a PDF document with client information, form content, and a signature."""
        self.pdf.add_page()


        # Add logo
        self.pdf.image(LOGO_FILE, w=25, x=15, y=11)

        # Print document text
        form_dict: Dict[str, Any] = self._get_json_dict(form_name)
        document: Document = Document(self.pdf, self.fonts,
                                        consent_flags, form_dict["document"])
        try:
            document.print()
        except RuntimeError as e:
            logging.error("Unable to print to pdf document: %s", e)

        # Space
        self.pdf.cell(0, 5, text = "", ln=True)

        # Add signature
        self._add_base64_image(siganture_base64, h=20)

        # Space
        self.pdf.cell(0, 5, text="", ln = True)

        # Add client's name
        self.pdf.cell(0, 5, text=client_name, ln=True, align="L")

        # Add date
        date: str = submit_datetime.strftime("%d %B %Y")
        self.pdf.cell(0, 5, text=date, ln=True, align="L")

        pdf_buffer: BytesIO = BytesIO()

        try:
            self.pdf.output(pdf_buffer)
        except RuntimeError as e:
            logging.error("Unable to output pdf document: %s", e)

        pdf_content: bytes = pdf_buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")

        logging.info("PDF successfully generated and encoded to base64")

        return pdf_base64

    def _get_json_dict(self, form_name: str) -> Dict[str, Any]:
        try:
            with open(f"{TEXT_FOLDER}/{form_name}.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error("Cannot read {form_name} config file: %s", e)
            raise
