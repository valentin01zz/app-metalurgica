from fpdf import FPDF
from fpdf.enums import XPos, YPos
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog
import os
import requests
from customtkinter import CTk, CTkButton, CTkLabel, set_appearance_mode, CTkFrame, CTkImage


def generar_pdf(nombre, telefono, tipo_persiana, desc, arreglo_medidasP,mano_obra):
    try:
        url = "https://dolarapi.com/v1/dolares/oficial"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ValorDolar = float(data["venta"])
        else:
            print("Error al obtener los datos:", response.status_code)
            ValorDolar = 1.0  # fallback
        
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        # Fondo color (por ejemplo, gris claro)
        pdf.set_fill_color(244, 231, 231)
        pdf.rect(x=0, y=0, w=210, h=297, style="F")  # A4: 210x297 mm
        # Encabezado
        pdf.set_fill_color(39, 38, 38)
        pdf.rect(x=0, y=0, w=210, h=40, style="F")
        
        # Insertar marca de agua
        marca_agua = os.path.join(os.path.dirname(__file__), 'fondoPDF.png')
        ancho_marca = 100
        alto_marca = 100
        x_centro = (pdf.w - ancho_marca) / 2
        y_centro = (pdf.h - alto_marca) / 2
        pdf.image(marca_agua, x=x_centro, y=y_centro, w=ancho_marca, h=alto_marca)

        # Encabezado
        pdf.set_font("Helvetica", 'B', 20)
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.now().strftime("%H:%M")
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, "CORTINERIA SAN JUAN", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.cell(0, 10, "PRESUPUESTO", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        imagen_logo = os.path.join(os.path.dirname(__file__), 'logosvg.png')
        ancho_imagen = 30
        pdf.image(imagen_logo, x=5, y=5, w=ancho_imagen,link='https://www.facebook.com/CORTINERIASANJUAN/')
        
        flechas_arribader = os.path.join(os.path.dirname(__file__), 'flechas.png')
        ancho_imagen = 50
        x = pdf.w - ancho_imagen
        pdf.image(flechas_arribader, x=x, y=0, w=ancho_imagen)
        pdf.image(flechas_arribader, x=x-15, y=0, w=ancho_imagen+15)
        pdf.ln(15)
        pdf.set_text_color(0,0,0)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(18, 10, "FECHA:")
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, fecha_actual, new_x=XPos.LMARGIN)
        
        pdf.set_x(pdf.w-pdf.r_margin-80)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(22, 10, "CORREO:")
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, "cortineriasanjuan@gmail.com", new_x=XPos.LMARGIN,new_y=YPos.NEXT)
        
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(22, 10, "CLIENTE:")
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, nombre, new_x=XPos.LMARGIN)
        
        pdf.set_x(pdf.w-pdf.r_margin-80)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(48, 10, "TELEFONO EMPRESA:")
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, "2645803651", new_x=XPos.LMARGIN,new_y=YPos.NEXT)
        
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(54, 10, "TELEFONO DEL CLIENTE:")
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, f"{telefono}", new_x=XPos.LMARGIN)

        pdf.set_x(pdf.w-pdf.r_margin-80)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(13, 10, "CUIT:")
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, f"20-34059962-5", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        """pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(33, 10, "VALOR DOLAR:")
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, f"${ValorDolar}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)"""

        pdf.ln(10)
    
        # Tabla encabezados
        pdf.set_fill_color(255, 191, 13)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(100, 10, "Descripcion", 1, align='C',	new_x=XPos.RIGHT, fill=True)
        pdf.cell(20, 10, "Cantidad", 1, align='C',	new_x=XPos.RIGHT, fill=True)
        pdf.cell(25, 10, "Medidas", 1, align='C',	new_x=XPos.RIGHT, fill=True)
        pdf.cell(30, 10, "Precio unitario", 1, align='C',new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)

        descripcion = f"{tipo_persiana}\n{desc}"
        pdf.set_font("Helvetica", '', 10)

        # La multi_cell en fpdf2 avanza la línea automáticamente
        # Guardamos la posición actual para poder alinear las otras celdas
        x = pdf.get_x()
        y = pdf.get_y()

        pdf.multi_cell(100, 5, descripcion, border=1)

        # Después de multi_cell, get_y() es el final del texto, la X vuelve al margen izquierdo
        y_final = pdf.get_y()

        # Posicionar celdas al lado derecho de la descripción (en la misma altura inicial)
        pdf.set_xy(x + 100, y)
        pdf.cell(20, 10, str(arreglo_medidasP[0][0]), 1, align='C',	new_x=XPos.RIGHT)
        pdf.cell(25, 10, str(arreglo_medidasP[0][1]), 1, align='C',	new_x=XPos.RIGHT)
        pdf.cell(30, 10, f"${arreglo_medidasP[0][2]}", 1, align='C',new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        total = arreglo_medidasP[0][0] * arreglo_medidasP[0][2]
        arreglo_medidasP.pop(0)

        for cantidad, medida, precio in arreglo_medidasP:
            x = pdf.get_x()
            y = pdf.get_y()
            # Dejar espacio vacío para la descripción
            pdf.multi_cell(100, 10, "", border=0)
            pdf.set_xy(x + 100, y)
            pdf.cell(20, 10, str(cantidad), 1, align='C',	new_x=XPos.RIGHT)
            pdf.cell(25, 10, str(medida), 1, align='C',	new_x=XPos.RIGHT)
            pdf.cell(30, 10, f"${precio}", 1, align='C',new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            total += float(precio) * cantidad
            
        total = total * mano_obra
        # Cálculo totales
        Total_30Porc = (30 / 100) * total
        Total_70Porc = (70 / 100) * total

        pdf.ln(10)
        x = pdf.get_x()
        y = pdf.get_y()

        pdf.cell(100, 10, "", 0, new_x=XPos.RIGHT)
        pdf.set_xy(x + 100, y + 5)
        pdf.cell(20, 10, "", 0, new_x=XPos.RIGHT)
        pdf.cell(25, 10, "", 0, new_x=XPos.RIGHT)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(30, 10, "Precio Dolares", 1, align='C',new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)

        # Observaciones, pagos y total
        x_inicio = pdf.get_x()
        y_inicio = pdf.get_y()
        pdf.rect(x_inicio, y_inicio, 90, 20)

        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(33, 10, "OBSERVACIONES:")
        pdf.set_font("Helvetica", '', 10)
        pdf.multi_cell(0, 10, "Precio sin IVA", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_xy(x + 100, y+15)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(20, 10, "70%:", 1, align='C',	new_x=XPos.RIGHT, fill=True)
        pdf.set_font("Helvetica", '', 10)
        pdf.cell(25, 10, f"${Total_70Porc:.2f}", 1, align='C',	new_x=XPos.RIGHT)
        pdf.cell(30, 10, f"${(Total_70Porc / ValorDolar):.2f}", 1, align='C',new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(42, 10, "DEMORA DE ENTREGA:")
        pdf.set_font("Helvetica", '', 10)
        pdf.cell(0, 10, "A acordar con el comprador", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_xy(x + 100, y)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(20, 10, "30%:", 1, align='C',	new_x=XPos.RIGHT, fill=True)
        pdf.set_font("Helvetica", '', 10)
        pdf.cell(25, 10, f"${Total_30Porc:.2f}", 1, align='C',	new_x=XPos.RIGHT)
        pdf.cell(30, 10, f"${(Total_30Porc / ValorDolar):.2f}", 1, align='C',new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.cell(100, 10, "", 0, new_x=XPos.RIGHT)
        pdf.set_xy(x + 100, y)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(20, 10, "Total:", 1, align='C',new_x=XPos.RIGHT, fill=True)
        pdf.set_font("Helvetica", '', 10)
        pdf.cell(25, 10, f"${total:.2f}", 1,align='C',	new_x=XPos.RIGHT)
        pdf.cell(30, 10, f"${(total / ValorDolar):.2f}", 1, align='C',new_x=XPos.LMARGIN, new_y=YPos.NEXT)


        #footer
        pdf.set_auto_page_break(auto=False)  # Desactiva el salto automático de página
        pdf.set_margins(0, 0, 0)            # Márgenes izquierdo, superior y derecho a 0

        pdf.set_fill_color(39, 38, 38)
        pdf.rect(x=0, y=277, w=210, h=30, style="F")

        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(0, 282)  # Ajusta esto si querés mover el texto verticalmente
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(210, 10, "-NO VÁLIDO COMO FACTURA-", align='C')

        # Guardar el PDF
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"boleta_{nombre}_{fecha_actual}_{hora_actual.replace(":","-")}hs.pdf"
        )
        if nombre_archivo:  # Solo si el usuario no canceló
            pdf.output(nombre_archivo)
            messagebox.showinfo("Éxito", f"Boleta generada exitosamente:\n{nombre_archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el PDF: {e}")