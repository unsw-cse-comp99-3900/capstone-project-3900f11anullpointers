"""Module for testing classes in doc_printing.py"""
import unittest
from unittest.mock import MagicMock
from fpdf import FPDF
from src.fonts.fonts import Fonts
from src.doc_printing import (
    Document,
    Title,
    InfoSection,
    ConsentSection,
    Sections,
    ConsentBody,
    Subtitle,
    Body,
)

class TestDocument(unittest.TestCase):
    """Class for testing the Document class"""
    def setUp(self):
        self.pdf = MagicMock(spec=FPDF)
        self.fonts = MagicMock(spec=Fonts)
        self.doc = {
            "title": "Testing Title",
            "sections": [
                {"type": "consent", "subtitle": "Subtitle", "body": "Body", "footnote": "Footnote"},
                {"type": "info", "subtitle": "Info subtitle", "body": "Info body"}
            ]
        }

        self.consent = [True]

    def test_doc_init(self):
        """Test the __init__ method"""
        document = Document(self.pdf, self.fonts, self.consent, self.doc)
        self.assertIsInstance(document.title, Title)
        self.assertIsInstance(document.sections, Sections)

    def test_print(self):
        """Test the print method"""
        document = Document(self.pdf, self.fonts, self.consent, self.doc)
        document.title.print = MagicMock()
        document.sections.print = MagicMock()
        document.print()
        document.title.print.assert_called_once()
        document.sections.print.assert_called_once()

class TestTitle(unittest.TestCase):
    """Class for testing the Title class"""
    def setUp(self):
        self.pdf = MagicMock(spec=FPDF)
        self.fonts = MagicMock(spec=Fonts)
        self.title_text = "Test Title"

    def test_print(self):
        """Test the print method"""
        title = Title(self.pdf, self.fonts, self.title_text)
        title.print()
        self.fonts.set_to_title.assert_called_once_with(self.pdf)
        self.pdf.cell.assert_called()

class TestInfoSection(unittest.TestCase):
    """Class for testing the InfoSection class"""
    def setUp(self):
        self.pdf = MagicMock(spec=FPDF)
        self.fonts = MagicMock(spec=Fonts)
        self.info = {"type": "int", "subtitle": "Info subtitle", "body": "Info body"}

    def test_print(self):
        """Test the print method"""
        info_section = InfoSection(self.pdf, self.fonts, self.info)
        info_section.subtitle.print = MagicMock()
        info_section.body.print = MagicMock()
        info_section.print()
        info_section.subtitle.print.assert_called_once()
        info_section.body.print.assert_called_once()

class TestConsentSection(unittest.TestCase):
    """Class for testing the ConsentSection class"""
    def setUp(self):
        self.pdf = MagicMock(spec=FPDF)
        self.fonts = MagicMock(spec=Fonts)
        self.info = {
            "type": "consent",
            "subtitle": "Subtitle",
            "body": "Body",
            "footnote": "Footnote"
        }
        self.info_no_footnote = {
            "type": "consent",
            "subtitle": "Subtitle",
            "body": "Body",
            "footnote": None
        }

    def test_print_footnote(self):
        """Test the print method with footnote"""
        consent_section = ConsentSection(self.pdf, self.fonts, True, self.info)
        consent_section.subtitle.print = MagicMock()
        consent_section.body.print = MagicMock()
        consent_section.footnote.print = MagicMock()
        consent_section.print()
        consent_section.subtitle.print.assert_called_once()
        consent_section.body.print.assert_called_once()
        consent_section.footnote.print.assert_called_once()

    def test_print_no_footnote(self):
        """Test the print method with no footnote"""
        consent_section = ConsentSection(self.pdf, self.fonts, True, self.info_no_footnote)
        consent_section.subtitle.print = MagicMock()
        consent_section.body.print = MagicMock()
        self.assertIsNone(consent_section.footnote)
        consent_section.print()
        consent_section.subtitle.print.assert_called_once()
        consent_section.body.print.assert_called_once()

class TestSections(unittest.TestCase):
    """Class for testing the Sections class"""
    def setUp(self):
        self.pdf = MagicMock(spec=FPDF)
        self.fonts = MagicMock(spec=Fonts)
        self.sections_data = [
            {"type": "info", "subtitle": "Info subtitle", "body": "Info body"},
            {
                "type": "consent",
                "subtitle": "Subtitle",
                "body": "Body",
                "footnote": "Footnote"
            }
        ]
        self.consent = [True]

    def test_sections_init(self):
        """Test the __init__ method"""
        sections = Sections(self.pdf, self.fonts, self.consent, self.sections_data)
        self.assertEqual(len(sections.sections), 2)
        self.assertIsInstance(sections.sections[0], InfoSection)
        self.assertIsInstance(sections.sections[1], ConsentSection)

    def test_print(self):
        """Test the print method"""
        sections = Sections(self.pdf, self.fonts, self.consent, self.sections_data)
        for section in sections.sections:
            section.print = MagicMock()
        sections.print()
        for section in sections.sections:
            section.print.assert_called_once()

class TestConsentBody(unittest.TestCase):
    """Class for testing the ConsentBody class"""
    def setUp(self):
        self.pdf = MagicMock(spec=FPDF)
        self.fonts = MagicMock(spec=Fonts)
        self.body_text = "Consent Body"

    def test_print_accepted(self):
        """Test the print method when consent is accepted"""
        body = ConsentBody(self.pdf, self.fonts, True, self.body_text)
        body.print()
        self.fonts.set_to_body_bold.assert_called_with(self.pdf)
        self.assertTrue(
            any(call[1]["text"] == "[X] I CONSENT" for call in self.pdf.cell.call_args_list)
        )
        self.assertTrue(
            any(call[1]["text"] == "[   ] I DO NOT CONSENT" for call in self.pdf.cell.call_args_list)
        )
        self.fonts.set_to_body.assert_called_with(self.pdf)
        self.assertTrue(
            any(call[1]["text"] == self.body_text for call in self.pdf.cell.call_args_list)
        )

    def test_print_not_accepted(self):
        """Test the print method when consent is not accepted"""
        body = ConsentBody(self.pdf, self.fonts, False, self.body_text)
        body.print()
        self.fonts.set_to_body_bold.assert_called_with(self.pdf)
        self.assertTrue(
            any(call[1]["text"] == "[   ] I CONSENT" for call in self.pdf.cell.call_args_list)
        )
        self.assertTrue(
            any(call[1]["text"] == "[X] I DO NOT CONSENT" for call in self.pdf.cell.call_args_list)
        )
        self.fonts.set_to_body.assert_called_with(self.pdf)
        self.assertTrue(
            any(call[1]["text"] == self.body_text for call in self.pdf.cell.call_args_list)
        )

class TestSubtitle(unittest.TestCase):
    """Class for testing the Subtitle class"""
    def setUp(self):
        self.pdf = MagicMock(spec=FPDF)
        self.fonts = MagicMock(spec=Fonts)
        self.subtitle = "Test subtitle"

    def test_print(self):
        """Test the print method"""
        subtitle = Subtitle(self.pdf, self.fonts, self.subtitle)
        subtitle.print()
        self.fonts.set_to_subtitle.assert_called_once_with(self.pdf)
        self.assertTrue(
            any(call[1]["text"] == self.subtitle for call in self.pdf.cell.call_args_list)
        )


class TestBody(unittest.TestCase):
    """Class for testing the Body class"""
    def setUp(self):
        self.pdf = MagicMock(spec=FPDF)
        self.fonts = MagicMock(spec=Fonts)
        self.body = "Test body"

    def test_print(self):
        """Test the print method"""
        body = Body(self.pdf, self.fonts, self.body)
        body.print()
        self.fonts.set_to_body.assert_called_once_with(self.pdf)

        self.assertTrue(
            any(call[1]["text"] == self.body for call in self.pdf.multi_cell.call_args_list)
        )


if __name__ == "__main__":
    unittest.main()
