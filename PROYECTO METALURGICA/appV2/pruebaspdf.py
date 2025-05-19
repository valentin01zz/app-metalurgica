from fpdf import FPDF
from tkinter import messagebox
import exception
from datetime import datetime
from tkinter import filedialog
import os
from customtkinter import CTk, CTkButton, CTkLabel

def generar_pdf(nombre, telefono,tipo_persiana,desc,arreglo_medidasP):
    try:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font("Arial",style="B", size=30)
        fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M")
        #ENCABEZADO
        imagen_logo=  os.path.join(os.path.dirname(__file__), 'logo3.png')
        pdf.cell(0, 10, txt="Presupuesto", ln=True, align='C')
        # 1. Calcular posición X (esquina derecha)
        ancho_pagina = pdf.w  # Ancho total de la página (ej: 210 mm en A4 vertical)
        ancho_imagen = 30  # Ancho deseado para la imagen
        margen_derecho = 10  # Margen derecho (en mm)
        x_pos = ancho_pagina - ancho_imagen - margen_derecho
        # 2. Insertar imagen en (x_pos, 10) -> 10 mm desde el borde superior
        pdf.image(imagen_logo, x=x_pos, y=10, w=ancho_imagen)
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt=f"FECHA: {fecha_hora_actual}", ln=True)
        pdf.cell(0, 10, txt=f"CLIENTE: {nombre}", ln=True)
        pdf.cell(0, 10, txt=f"TELEFONO: {telefono}", ln=True)
        #TABLA
        #cell(w, h, text, border, ln, align, fill): w: Ancho (0 = automático). h: Altura. border: 0=sin borde, 1=con borde. ln: 0=continuar en misma línea, 1=salto de línea. align: 'L' (izquierda), 'C' (centro), 'R' (derecha).fill: True para fondo coloreado.
        pdf.set_draw_color(255, 213, 30) # Color de borde
        pdf.set_fill_color(192,192,192) # Color de fondo
        pdf.cell(100, 10, "Descripcion",1, 0, 'C',True)
        pdf.cell(20, 10, "Cantidad", 1, 0, 'C',True)
        pdf.cell(30, 10, "Medidas", 1, 0, 'C',True)
        pdf.cell(30, 10, "Precio unitario", 1, 1, 'C',True)
        
        descripcion = f"{tipo_persiana} {desc}"
        pdf.set_font("Arial", size=10)
        # Celda de descripción con multi_cell para texto largo
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(100, 5, descripcion, 1, 'L')  # Alto de línea reducido a 5mm
        pdf.set_xy(x + 100, y)  # Posicionamos para la siguiente celda
        pdf.cell(20, 10,str(arreglo_medidasP[0][0]), 1, 0, 'C')
        pdf.cell(30,10,str(arreglo_medidasP[0][1]),1,0,'C')
        pdf.cell(30,10,f"${arreglo_medidasP[0][2]}",1,1,'C')
        total = arreglo_medidasP[0][0] * arreglo_medidasP[0][2]  # Calcular el total inicial
        arreglo_medidasP.pop(0)  # Eliminar la primera medida ya utilizada
        for cantidad,medida,precio in arreglo_medidasP:
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.multi_cell(100, 10, "", 0, 'L')  # Texto vacío
            pdf.set_xy(x + 100, y)  # Posicionar para siguientes celdas
            pdf.cell(20, 10, str(cantidad), 1, 0, 'C')
            pdf.cell(30,10,str(medida),1,0,'C')
            pdf.cell(30,10,f"${precio}",1,1,'C')
            total+= precio * cantidad
        
        #OBSERVACIONES, PRIMEROS PAGOS Y TOTAL
        pdf.ln(10)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.cell(100,10,"OBSERVACIONES: Precio sin IVA",0,0,'L')
        pdf.set_xy(x + 120, y)  # Posicionar para siguientes celdas
        pdf.cell(30,10,"70%:",1,0,'C',True)
        pdf.cell(30,10,f"${(70/100)*total}",1,1,'C')
        
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.cell(100,10,"DEMORA DE ENTREGA: A acordar con el comprador",0,0,'L')
        pdf.set_xy(x + 120, y)  # Posicionar para siguientes celdas
        pdf.cell(30,10,"$30%:",1,0,'C',True)
        pdf.cell(30,10,f"${(30/100)*total}",1,1,'C')
        
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.cell(100,10,"",0,0,'L')
        pdf.set_xy(x + 120, y)  # Posicionar para siguientes celdas
        pdf.cell(30,10,"Total:",1,0,'C',True)
        pdf.cell(30,10,f"${total:.2f}",1,1,'C')
        
        #Indicaciones finales
        pdf.ln(20)
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(255, 213, 30)
        pdf.multi_cell(0,4,"1_En el inicio del trabajo se solicita un adelanto, porcentaje sujeto según el trabajo a realizar. (aclarado en el presente documento.)",0,0,'C')
        pdf.ln(3)
        pdf.multi_cell(0,4,"2_El presupuesto y saldo son basados en las medidas iniciales (NO FINALES), por lo tanto, el presente es APROXIMADO y quedan sujetos a modificaciones al tomarse las medidas definitivas y herrajes adicionales de ser necesario, dicha modificación será sumada o restada del saldo final.)",0,0,'C')
        pdf.ln(3)
        pdf.multi_cell(0,4,"3_Las medidas finales serán tomadas con turno previo.)",0,0,'C')
        pdf.ln(3)
        pdf.multi_cell(0,4,"4_El plazo establecido de entrega es de 20 días APROXIMADAMENTE (dependiendo de la recepción de materia prima para elaborar el pedido) y según el trabajo solicitado, contando el plazo de entrega desde la fecha de toma de medidas finales.)",0,0,'C')
        pdf.ln(3)
        pdf.multi_cell(0,4,"5_El saldo final debe ser cancelado dentro de las 24hs de la finalización del trabajo, caso contrario sufrirá un incremento del 5% diario.)",0,0,'C')
        pdf.ln(3)
        pdf.cell(0, 10, "¡GRACIAS POR ELEGIRNOS!!!", ln=True, align='C')
        pdf.ln(3)
        pdf.set_font("Arial","B", size=10)
        pdf.cell(0, 10, "CORTINERA SAN JUAN  -  Teléfono: 264154657764  -  Email: cortineriasanjuan@gmail.com", ln=True, align='C')
        pdf.ln(3)
        pdf.cell(0, 10, "Direccion: Av. Ignacio de la Roza 1826 (o)", ln=True, align='C')
        # Guardar el PDF
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"boleta_{fecha_hora_actual}.pdf"
        )
        if nombre_archivo:  # Solo si el usuario no canceló
            pdf.output(nombre_archivo)
            messagebox.showinfo("Éxito", f"Boleta generada exitosamente:\n{nombre_archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el PDF: {e}")
if __name__ == "__main__":
    app= CTk()
    app.geometry("200x200")
    app.title("Generador de PDF")
    app.resizable(False,False)
    arreglo = [(1,"20x10",1000),(2,"30x50",2500),(1,"100x30,5",1200.60)]
    
    CTkLabel(app, text="Generador de PDF", text_color="black").pack(pady=10)
    CTkButton(app, text="Generar PDF", command=lambda: generar_pdf("Juan Perez", "123456789", "Persiana de madera","Paño aluminio inyectado con poliuretano expandido lama 45mm en medidas mas chicas y lamas de 77mm para medidas de 3,50 m y 2 m y 1,75 (estar tres con guias de chapa pintas coplor negro)Color negro. Automatizado con motor para tecla.Completas con herrajes y colocacion.s/instalacion electricas/control s/accionaniemto manual",arreglo), text_color="black").pack(pady=10)
    
    app.mainloop()