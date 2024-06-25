"""Module for printing documents to pdf"""
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from fpdf import FPDF
from backend.fonts.fonts import Fonts

class Document:
    """Document class"""
    def __init__(self, pdf: FPDF, fonts: Fonts, consent_flags: List[bool], doc: dict):
        self.pdf = pdf
        self.fonts = fonts
        self.title = Title(pdf, fonts, doc["title"])
        self.sections = Sections(pdf, fonts, consent_flags, doc["sections"])

    def print(self):
        """Prints the document to the pdf"""
        self.title.print()
        self.sections.print()

class Title:
    """Title class"""
    def __init__(self, pdf: FPDF, fonts: Fonts, title: str):
        self.pdf = pdf
        self.fonts = fonts
        self.title = title

    def print(self):
        """Prints the title to the pdf"""
        self.fonts.set_to_title(self.pdf)
        self.pdf.cell(200, 14, txt = self.title, ln = True, align = "C")
        # Space
        self.pdf.cell(0, 5, txt = "", ln = True)

class Section(ABC):
    """Section interface"""
    @abstractmethod
    def __init__(self, pdf: FPDF, fonts: Fonts, info: Dict[str, Any]):
        pass

    @abstractmethod
    def print(self):
        pass

class InfoSection(Section):
    """Infomation section class"""
    def __init__(self, pdf: FPDF, fonts: Fonts, info: Dict[str, Any]):
        self.pdf = pdf
        self.fonts = fonts
        self.subtitle = Subtitle(pdf, fonts, info["subtitle"])
        self.body = Body(pdf, fonts, info["body"])

    def print(self):
        self.subtitle.print()
        self.body.print()
        # Space
        self.pdf.cell(0, 6, txt = "", ln = True)

class ConsentSection(Section):
    """Consent section class"""
    def __init__(self, pdf: FPDF, fonts: Fonts, accepted: bool, info: Dict[str, Any]):
        self.pdf = pdf
        self.fonts = fonts
        self.subtitle = Subtitle(pdf, fonts, info["subtitle"])
        self.body = ConsentBody(pdf, fonts, accepted, info["body"])
        if info["footnote"] is None:
            self.footnote = None
        else:
            self.footnote = Body(pdf, fonts, info["footnote"])

    def print(self):
        """Prints the consent section to the pdf"""
        self.subtitle.print()
        self.body.print()
        # Space
        self.pdf.cell(0, 3, txt = "", ln = True)
        if self.footnote is not None:
            self.footnote.print()

        # Space
        self.pdf.cell(0, 6, txt = "", ln = True)

class Sections:
    """Sections class"""
    def __init__(self, pdf: FPDF, fonts: Fonts, consent_flags: List[bool],
                 sections: List[Dict[str, Any]]):
        self.pdf = pdf
        self.fonts = fonts
        self.sections = self._convert_to_sections(consent_flags, sections)

    def print(self):
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
    """Consent body class"""
    def __init__(self, pdf: FPDF, fonts: Fonts, accepted: bool, body: str):
        self.pdf = pdf
        self.fonts = fonts
        self.accepted = accepted
        self.body = body

    def print(self):
        """Prints the consent body to the pdf"""
        if self.accepted:
            self.fonts.set_to_body_bold(self.pdf)
            self.pdf.cell(24, 5, txt = "[X] I CONSENT", ln = 0, align = "L")
            self.fonts.set_to_body(self.pdf)
            self.pdf.cell(0, 5, txt = f"{self.body}", ln = True, align = "L")

            self.fonts.set_to_body_bold(self.pdf)
            self.pdf.cell(38, 5, txt = "[   ] I DO NOT CONSENT", ln = 0, align = "L")
            self.fonts.set_to_body(self.pdf)
            self.pdf.cell(0, 5, txt = f"{self.body}", ln = True, align = "L")
        else:
            self.fonts.set_to_body_bold(self.pdf)
            self.pdf.cell(24, 5, txt = "[   ] I CONSENT", ln = 0, align = "L")
            self.fonts.set_to_body(self.pdf)
            self.pdf.cell(0, 5, txt = f"{self.body}", ln = True, align = "L")

            self.fonts.set_to_body_bold(self.pdf)
            self.pdf.cell(38, 5, txt = "[X] I DO NOT CONSENT", ln = 0, align = "L")
            self.fonts.set_to_body(self.pdf)
            self.pdf.cell(0, 5, txt = f"{self.body}", ln = True, align = "L")

class Subtitle:
    """Subtitle class"""
    def __init__(self, pdf: FPDF, fonts: Fonts, subtitle: str):
        self.pdf = pdf
        self.fonts = fonts
        self.subtitle = subtitle

    def print(self):
        """Prints the subtitle to the pdf"""
        self.fonts.set_to_subtitle(self.pdf)
        self.pdf.cell(0, 5, txt = self.subtitle, ln = True, align = "L")
        # Space
        self.pdf.cell(0, 2, txt = "", ln = True)

class Body:
    """Body class"""
    def __init__(self, pdf: FPDF, fonts: Fonts, body: str):
        self.pdf = pdf
        self.fonts = fonts
        self.body = body

    def print(self):
        """Prints the body to the pdf"""
        self.fonts.set_to_body(self.pdf)
        self.pdf.multi_cell(0, 5, txt = self.body)
