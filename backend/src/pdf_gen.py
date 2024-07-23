"""PDF generator script

This module is responsible for generating consent form PDFs using the FPDF library. 
It defines the GeneratePDF class, which handles the creation and formatting of 
the PDF documents, including adding logo, signatures, and text content.

Classes:
- GeneratePDF: Handles the generation of a PDF document with consent information, 
  client signatures, and other details.

Functions:
- GeneratePDF.__init__: Initializes the PDF generator with necessary fonts.
- GeneratePDF._add_base64_image: Adds an image to the PDF from a base64-encoded string.
- GeneratePDF.generate_pdf: Generates a PDF document with client information, 
  form content, and a signature.
- GeneratePDF._get_json_dict: Retrieves the JSON configuration for the specified form.

Dependencies:
- json: For loading form configuration from JSON files.
- base64: For encoding and decoding base64 data.
- logging: For logging errors and information.
- datetime: For handling date and time.
- typing: For type hints.
- io: For handling in-memory byte streams.
- fpdf: The library used for PDF generation.
- .doc_printing: Module containing the Document class used for printing document content.
- .fonts.fonts: Module containing the Fonts class used for setting PDF fonts.

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

    def _add_base64_image(self, base64_data: str, h=None):
        if "base64," in base64_data:
            base64_data: str = base64_data.split("base64,")[1]

        image_data: bytes = base64.b64decode(base64_data)
        image_file: BytesIO = BytesIO(image_data)
        self.pdf.image(image_file, h=h)

    def generate_pdf(self, client_name: str, form_name: str,
                     consent_flags: List[bool], siganture_base64: str, submit_datetime: datetime) -> str:
        """Generates a PDF document with client information, form content, and a signature."""
        self.pdf.add_page()

        try:
            # Add logo
            self.pdf.image(LOGO_FILE, w=25, x=15, y=11)

            # Print document text
            form_dict: Dict[str, Any] = self._get_json_dict(form_name)
            document: Document = Document(self.pdf, self.fonts,
                                          consent_flags, form_dict["document"])
            document.print()

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

            pdf_buffer = BytesIO()
            self.pdf.output(pdf_buffer)

            pdf_content = pdf_buffer.getvalue()
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

            logging.info("PDF successfully generated and encoded to base64")

            return pdf_base64

        except Exception as e:
            logging.error("PDF generation failed: %s %s", e, type(e))
            raise


    def _get_json_dict(self, form_name: str) -> Dict[str, Any]:
        try:
            with open(f"{TEXT_FOLDER}/{form_name}.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error("Cannot read {form_name} config file: %s", e)
            raise
