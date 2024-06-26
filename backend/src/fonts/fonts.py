"""Fonts class"""
import json
import logging
from fpdf import FPDF

TITLE_SIZE = 16
SUBTITLE_SIZE = 14
BODY_SIZE = 10

FONTS_FOLDER = "fonts"
FONTS_FILE = "font_config.json"

class Fonts:
    """Loads fonts from FONT_CONFIG json file into class"""
    def __init__(self):
        try:
            with open(f"{FONTS_FOLDER}/{FONTS_FILE}", "r", encoding="utf-8") as file:
                font_dict = json.load(file)
                self.title = font_dict["title"]
                self.subtitle = font_dict["subtitle"]
                self.body = font_dict["body"]
                self.body_bold = font_dict["body_bold"]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error("Cannot read font config file: %s", e)
            raise

    def set_to_title(self, pdf: FPDF):
        """Sets current font to title font"""
        self._set_to_font(pdf, TITLE_SIZE, self.title)

    def set_to_subtitle(self, pdf: FPDF):
        """Sets current font to subtitle font"""
        self._set_to_font(pdf, SUBTITLE_SIZE, self.subtitle)

    def set_to_body(self, pdf: FPDF):
        """Sets current font to body font"""
        self._set_to_font(pdf, BODY_SIZE, self.body)

    def set_to_body_bold(self, pdf: FPDF):
        """Sets current font to body bold font"""
        self._set_to_font(pdf, BODY_SIZE, self.body_bold)

    def _set_to_font(self, pdf: FPDF, size: int, font_name: str):
        try:
            pdf.add_font(font_name, "", f"{FONTS_FOLDER}/{font_name}.ttf", uni=True)
            pdf.set_font(font_name, size=size)
        except RuntimeError as e:
            logging.error("Font %s not found: %s", font_name, e)
            raise
