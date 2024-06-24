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

def generate_pdf(token: str, client_name: str, form_name: str) -> None:
    """Generates a PDF document with the specified token, client name, and form name"""

    try:
        pdf = FPDF()
        pdf.add_page()

        fonts = get_fonts()

        # Generate title
        add_font(pdf, fonts["title"], 20)
        pdf.cell(200, 10, txt = get_title(form_name), ln = True, align = 'C')

        # Add logo
        pdf.image(LOGO_FILE, w=20, x=20, y=11)

        # Space
        pdf.cell(0, 8, txt = "", ln = True)

        # Generate subtitle
        add_font(pdf, fonts["subtitle"], 16)
        pdf.cell(200, 15, txt = get_subtitle(form_name), ln = True, align = 'L')

        # Generate text
        add_font(pdf, fonts["body"], 12)
        pdf.multi_cell(0, 5, txt = get_body(form_name))

        # Space
        pdf.cell(0, 15, txt = "", ln = True)

        # Add signature
        pdf.image(f"{SIGNATURE_FOLDER}/{token}.png", h = 20)

        # Space
        pdf.cell(0, 5, txt = "", ln = True)

        # Add client's name
        pdf.cell(0, 5, txt = client_name, ln = True, align = 'L')

        # Add date
        date: str = datetime.now().strftime("%d %B %Y")
        pdf.cell(0, 5, txt = date, ln = True, align = 'L')

        pdf.output(f"{token}.pdf")
        logging.info("%s.pdf successfully generated", token)

    except (RuntimeError, FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("PDF generation failed: %s", e)

def get_fonts() -> dict:
    """Loads fonts from FONT_CONFIG json file into dictionary"""

    try:
        with open(FONT_CONFIG, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("Cannot read font config file: %s", e)
        raise

def get_text(file_path: str) -> str:
    """Reads text from file_path into string"""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError as e:
        logging.error("Cannot read file %s: %s", file_path, e)
        raise

def add_font(pdf: FPDF, font_name: str, size: int) -> None:
    """Adds a font to a pdf"""

    try:
        pdf.add_font(font_name, "", f"{FONTS_FOLDER}/{font_name}.ttf", uni=True)
        pdf.set_font(font_name, size=size)
    except RuntimeError as e:
        logging.error("Font %s not found: %s", font_name, e)
        raise


def get_title(form_name: str) -> str:
    """Gets title text from saved file"""

    return get_text(f"{TEXT_FOLDER}/{form_name}/title.txt")

def get_subtitle(form_name: str) -> str:
    """Gets subtitle text from saved file"""

    return get_text(f"{TEXT_FOLDER}/{form_name}/subtitle.txt")

def get_body(form_name: str) -> str:
    """Gets body text from saved file"""

    return get_text(f"{TEXT_FOLDER}/{form_name}/body.txt")

def main():
    """Testing"""

    generate_pdf("test1", "Gerald", "consent1")


if __name__ == "__main__":
    main()
