"""
PDF generator script
"""

import json
from datetime import datetime
import logging
from fpdf import FPDF

TEXT_FOLDER = "form_text"
SIGNATURE_FOLDER = "signatures"
FONTS_FOLDER = "fonts"
LOGO_FOLDER = "logo"
FONT_CONFIG = f"{FONTS_FOLDER}/font_config.json"
LOGO_FILE = f"{LOGO_FOLDER}/logo.png"

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class GeneratePDF:
    """
    Class used to generate a consent form PDF
    """

    def __init__(self):
        self.pdf = FPDF()

    def generate_pdf(self, token: str, client_name: str, form_name: str) -> None:
        """Generates a PDF document with the specified token, client name, and form name"""

        try:
            self.pdf.add_page()

            fonts = self._get_fonts()

            # Generate title
            self._add_font(fonts["title"], 20)
            self.pdf.cell(200, 10, txt = self._get_title(form_name), ln = True, align = "C")

            # Add logo
            self.pdf.image(LOGO_FILE, w=20, x=20, y=11)

            # Space
            self.pdf.cell(0, 8, txt = "", ln = True)

            # Generate subtitle
            self._add_font(fonts["subtitle"], 16)
            self.pdf.cell(200, 15, txt = self._get_subtitle(form_name), ln = True, align = "L")

            # Generate text
            self._add_font(fonts["body"], 12)
            self.pdf.multi_cell(0, 5, txt = self._get_body(form_name))

            # Space
            self.pdf.cell(0, 15, txt = "", ln = True)

            # Add signature
            self.pdf.image(f"{SIGNATURE_FOLDER}/{token}.png", h = 20)

            # Space
            self.pdf.cell(0, 5, txt = "", ln = True)

            # Add client's name
            self.pdf.cell(0, 5, txt = client_name, ln = True, align = "L")

            # Add date
            date: str = datetime.now().strftime("%d %B %Y")
            self.pdf.cell(0, 5, txt = date, ln = True, align = "L")

            self.pdf.output(f"{token}.pdf")
            logging.info("%s.pdf successfully generated", token)

        except (RuntimeError, FileNotFoundError, json.JSONDecodeError) as e:
            logging.error("PDF generation failed: %s", e)

    def _get_fonts(self) -> dict:
        """Loads fonts from FONT_CONFIG json file into dictionary"""

        try:
            with open(FONT_CONFIG, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error("Cannot read font config file: %s", e)
            raise

    def _get_text(self, file_path: str) -> str:
        """Reads text from file_path into string"""

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        except FileNotFoundError as e:
            logging.error("Cannot read file %s: %s", file_path, e)
            raise

    def _add_font(self, font_name: str, size: int) -> None:
        """Adds a font to a pdf"""

        try:
            self.pdf.add_font(font_name, "", f"{FONTS_FOLDER}/{font_name}.ttf", uni=True)
            self.pdf.set_font(font_name, size=size)
        except RuntimeError as e:
            logging.error("Font %s not found: %s", font_name, e)
            raise


    def _get_title(self, form_name: str) -> str:
        """Gets title text from saved file"""

        return self._get_text(f"{TEXT_FOLDER}/{form_name}/title.txt")

    def _get_subtitle(self, form_name: str) -> str:
        """Gets subtitle text from saved file"""

        return self._get_text(f"{TEXT_FOLDER}/{form_name}/subtitle.txt")

    def _get_body(self, form_name: str) -> str:
        """Gets body text from saved file"""

        return self._get_text(f"{TEXT_FOLDER}/{form_name}/body.txt")

def main():
    """Testing"""
    generator = GeneratePDF()
    generator.generate_pdf("test1", "Gerald", "consent1")


if __name__ == "__main__":
    main()
