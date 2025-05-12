from fpdf import FPDF
from tkinter import messagebox
import exception
from datetime import datetime
from tkinter import filedialog
def generar_pdf(nombre, telefono, total,tipo_persiana):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Presupuesto", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Cliente: {nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Teléfono: {telefono}", ln=True)
        pdf.cell(200, 10, txt=f"Tipo persiana: {tipo_persiana}", ln=True)
        pdf.cell(200, 10, txt=f"Total: ${total:.2f}", ln=True)
        fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M")
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"boleta_{fecha_hora_actual}.pdf"
        )
        if nombre_archivo:  # Solo si el usuario no canceló
            pdf.output(nombre_archivo)
            messagebox.showinfo("Éxito", f"Boleta generada exitosamente:\n{nombre_archivo}")
    except exception as e:
        messagebox.showerror("Error", f"Error al generar el PDF: {e}")