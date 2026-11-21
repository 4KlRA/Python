from fpdf import FPDF

class Shirtfiticate(FPDF):

    def header(self):
        self.set_font("helvetica", style="B", size=45)
        self.cell(0, 60, "CS50 Shirtiicate", align="C", new_x="LMARGIN", new_y="NEXT")

def main():
    name = input("Name: ").split()
    create_shirtificate(name)

def create_shirtificate(name):
    pdf = Shirtfiticate(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    pdf.set_auto_page_break(auto=False)

    pdf.image("shirtificate.png", x="C", y=70, w=190)

    pdf.set_font("helvetica", size=24)
    pdf.set_y(140)
    pdf.cell(0, 10, f"{name} took CS50", align="C")

    pdf.output("shirtificate.pdf")

if __name__ == "__main__":
    main()