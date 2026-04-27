from fpdf import FPDF
from datetime import datetime
import os
import re

def limpiar_texto(texto: str) -> str:
    texto = texto.replace("**", "").replace("*", "").replace("`", "")
    texto = re.sub(r'[^\x00-\x7F\xC0-\xFF]', '', texto)
    return texto.strip()

def es_fila_tabla(linea: str) -> bool:
    return linea.startswith("|") and linea.endswith("|")

def es_separador_tabla(linea: str) -> bool:
    return es_fila_tabla(linea) and all(c in "|-: " for c in linea)

def parsear_fila(linea: str) -> list:
    celdas = linea.split("|")
    return [limpiar_texto(c) for c in celdas if c.strip()]

class OSINTPDFReport(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(0, 150, 0)
        self.set_x(15)
        self.cell(0, 10, "OSINT AI CLI - Informe de Reconocimiento", align="C")
        self.set_draw_color(0, 200, 0)
        self.line(10, 18, 200, 18)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(128, 128, 128)
        self.set_x(15)
        self.cell(0, 10, f"Solo para uso academico y educativo | Pagina {self.page_no()}", align="C")

def generar_pdf(dominio: str, contenido: str, nombre: str = None) -> str:
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
    pdf.cell(0, 12, f"Analisis OSINT: {dominio}", align="C")
    pdf.ln(6)

    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(100, 100, 100)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.set_x(15)
    pdf.cell(0, 6, f"Fecha de analisis: {fecha}", align="C")
    pdf.ln(4)
    pdf.set_x(15)
    pdf.cell(0, 6, "Herramienta: OSINT AI CLI | Proyecto Final IA Automatizacion 2025", align="C")
    pdf.ln(4)
    pdf.set_x(15)
    pdf.cell(0, 6, "Desarrollado por: Alba Mora", align="C")
    pdf.ln(8)

    pdf.set_draw_color(0, 150, 0)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(6)

    pdf.set_fill_color(255, 255, 200)
    pdf.set_text_color(150, 100, 0)
    pdf.set_font("DejaVu", "B", 9)
    pdf.set_x(15)
    pdf.cell(0, 7, "SOLO PARA USO ACADEMICO Y EDUCATIVO. El uso no autorizado es ilegal.",
             fill=True, align="C")
    pdf.ln(10)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", 10)

    lineas = contenido.split("\n")
    filas_tabla = []

    for linea in lineas:
        linea = linea.strip()

        if es_fila_tabla(linea):
            if not es_separador_tabla(linea):
                filas_tabla.append(parsear_fila(linea))
            continue

        if filas_tabla:
            headers = filas_tabla[0]
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
                for fila in filas_tabla[1:]:
                    pdf.set_x(15)
                    for i, celda in enumerate(fila):
                        if i < len(headers):
                            pdf.cell(col_width, 6, celda[:35], border=1)
                    pdf.ln()
                pdf.ln(4)
            filas_tabla = []

        if not linea:
            pdf.ln(3)
            continue

        if linea.startswith("## "):
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 13)
            pdf.set_text_color(0, 100, 0)
            pdf.set_x(15)
            pdf.multi_cell(0, 8, limpiar_texto(linea.replace("## ", "").replace("#", "")))
            pdf.set_draw_color(0, 180, 0)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(3)
            pdf.set_font("DejaVu", "", 10)
            pdf.set_text_color(0, 0, 0)

        elif linea.startswith("# "):
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 15)
            pdf.set_text_color(0, 80, 0)
            pdf.set_x(15)
            pdf.multi_cell(0, 9, limpiar_texto(linea.replace("# ", "")))
            pdf.ln(2)
            pdf.set_font("DejaVu", "", 10)
            pdf.set_text_color(0, 0, 0)

        elif linea.startswith("### "):
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_text_color(0, 120, 0)
            pdf.set_x(15)
            pdf.multi_cell(0, 7, limpiar_texto(linea.replace("### ", "")))
            pdf.ln(2)
            pdf.set_font("DejaVu", "", 10)
            pdf.set_text_color(0, 0, 0)

        elif linea.startswith("- ") or linea.startswith("• "):
            texto = limpiar_texto(linea.replace("- ", "").replace("• ", ""))
            pdf.set_font("DejaVu", "", 10)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, f"- {texto}")

        elif len(linea) > 2 and linea[0].isdigit() and linea[1] in [".", ")"]:
            texto = limpiar_texto(linea[2:])
            pdf.set_font("DejaVu", "", 10)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, f"{linea[:2]} {texto}")

        elif linea.startswith("---"):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)

        else:
            texto = limpiar_texto(linea)
            if texto:
                pdf.set_font("DejaVu", "", 10)
                pdf.set_x(15)
                pdf.multi_cell(0, 6, texto)

    if filas_tabla:
        headers = filas_tabla[0]
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
            for fila in filas_tabla[1:]:
                pdf.set_x(15)
                for i, celda in enumerate(fila):
                    if i < len(headers):
                        pdf.cell(col_width, 6, celda[:35], border=1)
                pdf.ln()

    os.makedirs("informes", exist_ok=True)
    if nombre:
        nombre = nombre.replace(" ", "_")
        if not nombre.endswith(".pdf"):
            nombre += ".pdf"
        nombre_fichero = f"informes/{nombre}"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_fichero = f"informes/osint_{dominio}_{timestamp}.pdf"

    pdf.output(nombre_fichero)
    return nombre_fichero