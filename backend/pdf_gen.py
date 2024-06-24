from fpdf import FPDF
import json
from datetime import datetime

FONT_CONFIG = "font_config.json"
TEXT_FOLDER = "form_text/"
SIGNATURE_FOLDER = "signatures/"
LOGO_FILE = "logo/logo.png"

def generate_PDF(token: str, name: str, form_name: str) -> None:
    pdf: object = FPDF()
    pdf.add_page()

    fonts = get_fonts()
    
    # Generate title
    pdf.add_font(fonts["title"], "", "fonts/" + fonts["title"] + ".ttf", uni=True)
    pdf.set_font(fonts["title"], size=20)
    pdf.cell(200, 10, txt = get_title(form_name), ln = True, align = 'C')

    # Add logo
    pdf.image(LOGO_FILE, w=20, x=20, y=11)

    # Space
    pdf.cell(0, 8, txt = "", ln = True)

    # Generate subtitle
    pdf.add_font(fonts["subtitle"], "", "fonts/" + fonts["subtitle"] + ".ttf", uni=True)
    pdf.set_font(fonts["subtitle"], size=16)
    pdf.cell(200, 15, txt = get_subtitle(form_name), ln = True, align = 'L')

    # Generate text
    pdf.add_font(fonts["body"], "", "fonts/" + fonts["body"] + ".ttf", uni=True)
    pdf.set_font(fonts["body"], size=12)
    pdf.multi_cell(0, 5, txt = get_body(form_name))

    # Space
    pdf.cell(0, 15, txt = "", ln = True)

    # Add signature
    pdf.image(SIGNATURE_FOLDER + token + ".png", w = 80, h = 20)

    # Space
    pdf.cell(0, 5, txt = "", ln = True)

    # Add clinet's name
    pdf.cell(0, 5, txt = name, ln = True, align = 'L')

    # Add date
    date: str = datetime.now().strftime("%d %B %Y")
    pdf.cell(0, 5, txt = date, ln = True, align = 'L')

    pdf.output(token + ".pdf")
    

def get_fonts() -> dict:
    with open(FONT_CONFIG, "r") as file:
        fonts = json.load(file)

    return fonts

def get_title(form_name: str) -> str:
    with open(TEXT_FOLDER + form_name + "/title.txt", "r") as file:
        title = file.read()

    return title

def get_subtitle(form_name: str) -> str:
    with open(TEXT_FOLDER + form_name + "/subtitle.txt", "r") as file:
        subtitle = file.read()

    return subtitle

def get_body(form_name: str) -> str:
    with open(TEXT_FOLDER + form_name + "/body.txt", "r") as file:
        text = file.read()

    return text


def main():
    generate_PDF("test1", "Gerald", "consent1")


if __name__ == "__main__":
    main()


    