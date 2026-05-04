from fpdf import FPDF
from datetime import datetime
import os
import re

def clean_text(text: str) -> str:
    text = text.replace("**", "").replace("*", "").replace("`", "")
    text = re.sub(r'[^\x00-\x7F\xC0-\xFF]', '', text)
    return text.strip()

def is_table_row(line: str) -> bool:
    return line.startswith("|") and line.endswith("|")

def is_table_separator(line: str) -> bool:
    return is_table_row(line) and all(c in "|-: " for c in line)

def parse_row(line: str) -> list:
    cells = line.split("|")
    return [clean_text(c) for c in cells if c.strip()]

class OSINTPDFReport(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(0, 150, 0)
        self.set_x(15)
        self.cell(0, 10, "OSINT AI CLI - Reconnaissance Report", align="C")
        self.set_draw_color(0, 200, 0)
        self.line(10, 18, 200, 18)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(128, 128, 128)
        self.set_x(15)
        self.cell(0, 10, f"For academic and educational use only | Page {self.page_no()}", align="C")

def generate_pdf(domain: str, content: str, name: str = None) -> str:
    pdf = OSINTPDFReport()
    pdf.add_font("DejaVu", "", "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVu", "I", "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Oblique.ttf")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    pdf.set_font("DejaVu", "B", 18)
    pdf.set_text_color(0, 100, 0)
    pdf.set_x(15)
    pdf.cell(0, 12, f"OSINT Analysis: {domain}", align="C")
    pdf.ln(6)

    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(100, 100, 100)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.set_x(15)
    pdf.cell(0, 6, f"Analysis date: {date}", align="C")
    pdf.ln(4)
    pdf.set_x(15)
    pdf.cell(0, 6, "Tool: OSINT AI CLI | Final Project AI Automation 2026", align="C")
    pdf.ln(4)
    pdf.set_x(15)
    pdf.cell(0, 6, "Developed by: Alba Mora", align="C")
    pdf.ln(8)

    pdf.set_draw_color(0, 150, 0)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(6)

    pdf.set_fill_color(255, 255, 200)
    pdf.set_text_color(150, 100, 0)
    pdf.set_font("DejaVu", "B", 9)
    pdf.set_x(15)
    pdf.cell(0, 7, "FOR ACADEMIC AND EDUCATIONAL USE ONLY.",
             fill=True, align="C")
    pdf.ln(10)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", 10)

    lines = content.split("\n")
    table_rows = []

    for line in lines:
        line = line.strip()

        if is_table_row(line):
            if not is_table_separator(line):
                table_rows.append(parse_row(line))
            continue

        if table_rows:
            headers = table_rows[0]
            if headers:
                col_width = (pdf.w - 30) / len(headers)
                pdf.set_font("DejaVu", "B", 9)
                pdf.set_fill_color(200, 230, 200)
                pdf.set_text_color(0, 80, 0)
                pdf.set_x(15)
                for h in headers:
                    pdf.cell(col_width, 7, h[:35], border=1, fill=True)
                pdf.ln()
                pdf.set_font("DejaVu", "", 9)
                pdf.set_fill_color(255, 255, 255)
                pdf.set_text_color(0, 0, 0)
                for row in table_rows[1:]:
                    pdf.set_x(15)
                    for i, cell in enumerate(row):
                        if i < len(headers):
                            pdf.cell(col_width, 6, cell[:35], border=1)
                    pdf.ln()
                pdf.ln(4)
            table_rows = []

        if not line:
            pdf.ln(3)
            continue

        if line.startswith("## "):
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 13)
            pdf.set_text_color(0, 100, 0)
            pdf.set_x(15)
            pdf.multi_cell(0, 8, clean_text(line.replace("## ", "").replace("#", "")))
            pdf.set_draw_color(0, 180, 0)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(3)
            pdf.set_font("DejaVu", "", 10)
            pdf.set_text_color(0, 0, 0)

        elif line.startswith("# "):
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 15)
            pdf.set_text_color(0, 80, 0)
            pdf.set_x(15)
            pdf.multi_cell(0, 9, clean_text(line.replace("# ", "")))
            pdf.ln(2)
            pdf.set_font("DejaVu", "", 10)
            pdf.set_text_color(0, 0, 0)

        elif line.startswith("### "):
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_text_color(0, 120, 0)
            pdf.set_x(15)
            pdf.multi_cell(0, 7, clean_text(line.replace("### ", "")))
            pdf.ln(2)
            pdf.set_font("DejaVu", "", 10)
            pdf.set_text_color(0, 0, 0)

        elif line.startswith("- ") or line.startswith("• "):
            text = clean_text(line.replace("- ", "").replace("• ", ""))
            pdf.set_font("DejaVu", "", 10)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, f"- {text}")

        elif len(line) > 2 and line[0].isdigit() and line[1] in [".", ")"]:
            text = clean_text(line[2:])
            pdf.set_font("DejaVu", "", 10)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, f"{line[:2]} {text}")

        elif line.startswith("---"):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)

        else:
            text = clean_text(line)
            if text:
                pdf.set_font("DejaVu", "", 10)
                pdf.set_x(15)
                pdf.multi_cell(0, 6, text)

    if table_rows:
        headers = table_rows[0]
        if headers:
            col_width = (pdf.w - 30) / len(headers)
            pdf.set_font("DejaVu", "B", 9)
            pdf.set_fill_color(200, 230, 200)
            pdf.set_text_color(0, 80, 0)
            pdf.set_x(15)
            for h in headers:
                pdf.cell(col_width, 7, h[:35], border=1, fill=True)
            pdf.ln()
            pdf.set_font("DejaVu", "", 9)
            pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(0, 0, 0)
            for row in table_rows[1:]:
                pdf.set_x(15)
                for i, cell in enumerate(row):
                    if i < len(headers):
                        pdf.cell(col_width, 6, cell[:35], border=1)
                pdf.ln()

    os.makedirs("reports", exist_ok=True)
    if name:
        name = name.replace(" ", "_")
        if not name.endswith(".pdf"):
            name += ".pdf"
        file_name = f"reports/{name}"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"pdf_reports/osint_{domain}_{timestamp}.pdf"

    pdf.output(file_name)
    return file_name