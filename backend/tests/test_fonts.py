"""Module for testing fonts.py"""
import unittest
from unittest.mock import mock_open, patch, MagicMock
import json
from fpdf import FPDF
from src.fonts.fonts import (
    Fonts,
    TITLE_SIZE,
    SUBTITLE_SIZE,
    BODY_SIZE,
    FONTS_FOLDER,
    FONTS_FILE,
)

class TestFonts(unittest.TestCase):
    """Class for testing the Fonts class"""
    def setUp(self):
        self.pdf_mock = MagicMock(spec=FPDF)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
            "title": "TitleFont",
            "subtitle": "SubtitleFont",
            "body": "BodyFont",
            "body_bold": "BodyBoldFont"
        }))
    def test_init_success(self, mock_file):
        """Test if fonts are added correctly to the class"""
        fonts = Fonts()
        self.assertEqual(fonts.title, "TitleFont")
        self.assertEqual(fonts.subtitle, "SubtitleFont")
        self.assertEqual(fonts.body, "BodyFont")
        self.assertEqual(fonts.body_bold, "BodyBoldFont")
        mock_file.assert_called_once_with(f"{FONTS_FOLDER}/{FONTS_FILE}", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_init_json_decode_error(self, _):
        """Test JSON decode error is raised when invalid json is used"""
        with self.assertRaises(json.JSONDecodeError):
            Fonts()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_init_file_not_found_error(self, _):
        """Test file not found error when the file is missing"""
        with self.assertRaises(FileNotFoundError):
            Fonts()

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
            "title": "TitleFont",
            "subtitle": "SubtitleFont",
            "body": "BodyFont",
            "body_bold": "BodyBoldFont"
        }))
    def test_set_to_title(self, _):
        """Test the set_to_title method"""
        fonts = Fonts()
        fonts.set_to_title(self.pdf_mock)
        self.pdf_mock.add_font.assert_called_once_with("TitleFont", "",
                                                       f"{FONTS_FOLDER}/TitleFont.ttf", uni=True)
        self.pdf_mock.set_font.assert_called_once_with("TitleFont", size=TITLE_SIZE)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
            "title": "TitleFont",
            "subtitle": "SubtitleFont",
            "body": "BodyFont",
            "body_bold": "BodyBoldFont"
        }))
    def test_set_to_subtitle(self, _):
        """Test the set_to_subtitle method"""
        fonts = Fonts()
        fonts.set_to_subtitle(self.pdf_mock)
        self.pdf_mock.add_font.assert_called_once_with("SubtitleFont", "",
                                                       f"{FONTS_FOLDER}/SubtitleFont.ttf", uni=True)
        self.pdf_mock.set_font.assert_called_once_with("SubtitleFont", size=SUBTITLE_SIZE)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
            "title": "TitleFont",
            "subtitle": "SubtitleFont",
            "body": "BodyFont",
            "body_bold": "BodyBoldFont"
        }))
    def test_set_to_body(self, _):
        """Test the set_to_body method"""
        fonts = Fonts()
        fonts.set_to_body(self.pdf_mock)
        self.pdf_mock.add_font.assert_called_once_with("BodyFont", "",
                                                       f"{FONTS_FOLDER}/BodyFont.ttf", uni=True)
        self.pdf_mock.set_font.assert_called_once_with("BodyFont", size=BODY_SIZE)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
            "title": "TitleFont",
            "subtitle": "SubtitleFont",
            "body": "BodyFont",
            "body_bold": "BodyBoldFont"
        }))
    def test_set_to_body_bold(self, _):
        """Test the set_to_bold_body method"""
        fonts = Fonts()
        fonts.set_to_body_bold(self.pdf_mock)
        self.pdf_mock.add_font.assert_called_once_with("BodyBoldFont", "",
                                                       f"{FONTS_FOLDER}/BodyBoldFont.ttf", uni=True)
        self.pdf_mock.set_font.assert_called_once_with("BodyBoldFont", size=BODY_SIZE)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
            "title": "TitleFont",
            "subtitle": "SubtitleFont",
            "body": "BodyFont",
            "body_bold": "BodyBoldFont"
        }))
    def test_set_to_font_runtime_error(self, _):
        """Test if a runtime error is encountered when a font is not found"""
        self.pdf_mock.add_font.side_effect = RuntimeError("Font not found")
        fonts = Fonts()
        with self.assertRaises(RuntimeError):
            fonts.set_to_title(self.pdf_mock)

if __name__ == "__main__":
    unittest.main()
