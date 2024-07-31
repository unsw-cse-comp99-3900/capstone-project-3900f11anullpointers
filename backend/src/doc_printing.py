"""Module for printing documents to pdf.

This module defines the structure and behavior of a PDF document generation system 
using the FPDF library. It includes classes for creating and formatting various 
sections of a document such as titles, subtitles, body text, and consent sections.

Classes:
- Document: Manages the overall document structure, including the title and sections.
- Title: Handles the title of the document.
- Section (ABC): Abstract base class for different types of sections in the document.
- InfoSection: Concrete implementation of Section for informational content.
- ConsentSection: Concrete implementation of Section for consent information.
- Sections: Manages a collection of sections in the document.
- ConsentBody: Manages the body for consent sections, with options for accepted or not accepted.
- Subtitle: Handles the subtitle of sections.
- Body: Handles the body content of sections.

Dependencies:
- FPDF: The library used for PDF generation.
- Fonts: Custom font settings for the PDF.
- typing: Used for type hinting.
- abc: Provides the abstract base class functionality.
"""
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from fpdf import FPDF
from .fonts.fonts import Fonts

class Document:
    """Manages the overall document structure, including the title and sections."""
    def __init__(self, pdf: FPDF, fonts: Fonts, consent_flags: List[bool], doc: dict):
        self.pdf = pdf
        self.fonts = fonts
        self.title = Title(pdf, fonts, doc["title"])
        self.sections = Sections(pdf, fonts, consent_flags, doc["sections"])

    def print(self) -> None:
        """Prints the document to the pdf"""
        self.title.print()
        self.sections.print()

class Title:
    """Handles the title of the document."""
    def __init__(self, pdf: FPDF, fonts: Fonts, title: str):
        self.pdf = pdf
        self.fonts = fonts
        self.title = title

    def print(self) -> None:
        """Prints the title to the pdf"""
        self.fonts.set_to_title(self.pdf)
        self.pdf.cell(200, 14, text = self.title, ln = True, align = "C")
        # Space
        self.pdf.cell(0, 5, text = "", ln = True)

class Section(ABC):
    """Abstract base class for different types of sections in the document."""
    @abstractmethod
    def __init__(self, pdf: FPDF, fonts: Fonts, info: Dict[str, Any]):
        pass

    @abstractmethod
    def print(self) -> None:
        pass

class InfoSection(Section):
    """Concrete implementation of Section for informational content."""
    def __init__(self, pdf: FPDF, fonts: Fonts, info: Dict[str, Any]):
        self.pdf = pdf
        self.fonts = fonts
        self.subtitle = Subtitle(pdf, fonts, info["subtitle"])
        self.body = Body(pdf, fonts, info["body"])

    def print(self) -> None:
        """Prints the info section to the pdf"""
        self.subtitle.print()
        self.body.print()
        # Space
        self.pdf.cell(0, 6, text = "", ln = True)

class ConsentSection(Section):
    """Concrete implementation of Section for consent information."""
    def __init__(self, pdf: FPDF, fonts: Fonts, accepted: bool, info: Dict[str, Any]):
        self.pdf = pdf
        self.fonts = fonts
        self.subtitle = Subtitle(pdf, fonts, info["subtitle"])
        self.body = ConsentBody(pdf, fonts, accepted, info["body"])
        if info["footnote"] is None:
            self.footnote = None
        else:
            self.footnote = Body(pdf, fonts, info["footnote"])

    def print(self) -> None:
        """Prints the consent section to the pdf"""
        self.subtitle.print()
        self.body.print()
        # Space
        self.pdf.cell(0, 3, text = "", ln = True)
        if self.footnote is not None:
            self.footnote.print()

        # Space
        self.pdf.cell(0, 6, text = "", ln = True)

class Sections:
    """Manages a collection of sections in the document."""
    def __init__(self, pdf: FPDF, fonts: Fonts, consent_flags: List[bool],
                 sections: List[Dict[str, Any]]):
        self.pdf = pdf
        self.fonts = fonts
        self.sections = self._convert_to_sections(consent_flags, sections)

    def print(self) -> None:
        """Prints the sections to the pdf"""
        for section in self.sections:
            section.print()

    def _convert_to_sections(self, consent_flags: List[bool],
                             sections: List[Dict[str, Any]]) -> List[Section]:
        output = []
        i = 0
        for section in sections:
            if section["type"] == "info":
                output.append(InfoSection(self.pdf, self.fonts, section))
            if section["type"] == "consent":
                if i < len(consent_flags):
                    output.append(ConsentSection(self.pdf, self.fonts, consent_flags[i], section))
                else: # If no bool has been recorded default to no consent
                    output.append(ConsentSection(self.pdf, self.fonts, False, section))
                i += 1

        return output

class ConsentBody:
    """Manages the body for consent sections, with options for accepted or not accepted."""
    def __init__(self, pdf: FPDF, fonts: Fonts, accepted: bool, body: str):
        self.pdf = pdf
        self.fonts = fonts
        self.accepted = accepted
        self.body = body

    def print(self) -> None:
        """Prints the consent body to the pdf"""
        if self.accepted:
            self.fonts.set_to_body_bold(self.pdf)
            self.pdf.cell(24, 5, text = "[X] I CONSENT", ln = 0, align = "L")
            self.fonts.set_to_body(self.pdf)
            self.pdf.cell(0, 5, text = f"{self.body}", ln = True, align = "L")

            self.fonts.set_to_body_bold(self.pdf)
            self.pdf.cell(38, 5, text = "[   ] I DO NOT CONSENT", ln = 0, align = "L")
            self.fonts.set_to_body(self.pdf)
            self.pdf.cell(0, 5, text = f"{self.body}", ln = True, align = "L")
        else:
            self.fonts.set_to_body_bold(self.pdf)
            self.pdf.cell(24, 5, text = "[   ] I CONSENT", ln = 0, align = "L")
            self.fonts.set_to_body(self.pdf)
            self.pdf.cell(0, 5, text = f"{self.body}", ln = True, align = "L")

            self.fonts.set_to_body_bold(self.pdf)
            self.pdf.cell(38, 5, text = "[X] I DO NOT CONSENT", ln = 0, align = "L")
            self.fonts.set_to_body(self.pdf)
            self.pdf.cell(0, 5, text = f"{self.body}", ln = True, align = "L")

class Subtitle:
    """Handles the subtitle of sections."""
    def __init__(self, pdf: FPDF, fonts: Fonts, subtitle: str):
        self.pdf = pdf
        self.fonts = fonts
        self.subtitle = subtitle

    def print(self) -> None:
        """Prints the subtitle to the pdf"""
        self.fonts.set_to_subtitle(self.pdf)
        self.pdf.cell(0, 5, text = self.subtitle, ln = True, align = "L")
        # Space
        self.pdf.cell(0, 2, text = "", ln = True)

class Body:
    """Handles the body content of sections."""
    def __init__(self, pdf: FPDF, fonts: Fonts, body: str):
        self.pdf = pdf
        self.fonts = fonts
        self.body = body

    def print(self) -> None:
        """Prints the body to the pdf"""
        self.fonts.set_to_body(self.pdf)
        self.pdf.multi_cell(0, 5, text = self.body)
