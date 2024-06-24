from fpdf import FPDF

def generate_PDF(token: str, name: str, form_name: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    
    with open("form_text/" + form_name + "/title.txt", "r") as file:
        title = file.read()

    with open("form_text/" + form_name + "/subtitle.txt", "r") as file:
        subtitle = file.read()

    with open("form_text/" + form_name + "/text.txt", "r") as file:
        text = file.read()
    
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt = title, ln = True, align = 'C')

    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt = subtitle, ln = True, align = 'L')

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 5, txt = text)

    pdf.output(token + ".pdf")


def main():
    generate_PDF("test1", "gerald", "consent1")


if __name__ == "__main__":
    main()


    