import customtkinter as ctk
import tkinter as tk
import requests
import csv
import time
import webbrowser
from fpdf import FPDF
import messagebox

class Material():
    __nombre: str
    __descripcion: float
    def __init__(self, nombre, descripcion):
        self.__nombre = nombre
        self.__descripcion = descripcion
    def __str__(self):
        return f"Nombre: {self.__nombre}, descripcion: {self.__descripcion}"
    def get_nom(self):
        return self.__nombre
    def get_descripcion(self):           
        return self.__descripcion
class gestor_materiales():
    __materiales: list
    def __init__(self, materiales = []):
        self.__materiales = materiales
    def cargar_materiales(self):
        with open("C:\\Users\\gilva\\Desktop\\Proyectos\\app-metalurgica-main\\app-metalurgica-main\\PROYECTO METALURGICA\\pruebas\\materiales.csv", newline='', encoding='utf-8') as archivo_csv: 
            reader = csv.reader(archivo_csv,delimiter=';') 
            next(reader)
            next(reader)
            for fila in reader: 
                self.__materiales.append(Material(fila[0],str(fila[1])))
            for material in self.__materiales: print(material)
    def get_materiales(self):
        return self.__materiales
GM = gestor_materiales()
GM.cargar_materiales()
def abrir_web_factura():
    webbrowser.open("https://www.arca.gob.ar/fe/")
url = "https://dolarapi.com/v1/dolares/oficial"
# Hacer la solicitud GET
response = requests.get(url)
# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
    compra = data["compra"]
    venta = data["venta"]
    fecha = data["fechaActualizacion"]
else:
    print("Error al obtener los datos:", response.status_code)

app = ctk.CTk()
app.title("Generador de Boletas")
app.state('zoomed')
def ventana_recibo():
    ventana = ctk.CTkToplevel(app)
    ventana.title("Recibo")
    ventana.geometry("500x500")
    ventana.resizable(False, False)
    ventana.transient(app)  # Hace que esta ventana dependa de la principal
    ventana.grab_set()  # Hace que la ventana sea modal

    # Etiqueta para mostrar los valores del dólar
    label_dolar = ctk.CTkLabel(
        ventana,
        text=f"Compra: {compra}\nVenta: {venta}",
        text_color="black",
        font=("Arial", 20),
        fg_color="#2F1205"
    )
    label_dolar.pack(pady=20)

    # Boton para Persianas Metalicas
    def persianas_metalicas():
        ventana_presupuesto("Persianas Metálicas")

    boton_metalicas = ctk.CTkButton(
        ventana,
        text='Persianas Metalicas',
        command=persianas_metalicas,
        fg_color='#005f73',
        hover_color='#0a9396',
        text_color='white'
    )
    boton_metalicas.pack(pady=10)

    # Boton para Persianas de Aluminio
    def persianas_aluminio():
        ventana_presupuesto("Persianas de Aluminio")

    boton_aluminio = ctk.CTkButton(
        ventana,
        text="Persianas de Aluminio",
        command=persianas_aluminio,
        fg_color="#9b2226",
        hover_color="#ae2012",
        text_color="white"
    )
    boton_aluminio.pack(pady=10)

# Boton principal para abrir la ventana de recibo
button_recibo = ctk.CTkButton(
    app,
    text="Recibo",
    command=ventana_recibo,
    fg_color="#000000",
    hover_color="lightgray",
    text_color="red"
)
button_recibo.pack()

# Boton para abrir la pagina de facturacion
button_factura = ctk.CTkButton(
    app,
    text="Factura",
    command=abrir_web_factura
)
button_factura.pack()

def ventana_presupuesto(tipo_persiana):
    ventana = ctk.CTkToplevel(app)
    ventana.title(f"Presupuesto - {tipo_persiana}")
    ventana.geometry("600x700")
    ventana.resizable(False, False)
    ventana.transient(app)
    ventana.grab_set()

    label_titulo = ctk.CTkLabel(
        ventana,
        text=f"Presupuesto para {tipo_persiana}",
        font=('Arial', 18)
    )
    label_titulo.pack(pady=10)

    # Campo para el nombre del cliente
    label_nombre = ctk.CTkLabel(ventana, text="Nombre del Cliente:")
    label_nombre.pack(pady=5)
    entry_nombre = ctk.CTkEntry(ventana, width=300)
    entry_nombre.pack(pady=5)

    # Campo para el numero de teléfono
    label_telefono = ctk.CTkLabel(ventana, text="Numero de Teléfono:")
    label_telefono.pack(pady=5)
    entry_telefono = ctk.CTkEntry(ventana, width=300)
    entry_telefono.pack(pady=5)

    # Campo para el precio del material
    label_precio = ctk.CTkLabel(ventana, text="Precio del Material:")
    label_precio.pack(pady=5)
    entry_precio = ctk.CTkEntry(ventana, width=300)
    entry_precio.pack(pady=5)

    # Campo para el precio de la mano de obra
    label_mano_obra = ctk.CTkLabel(ventana, text="Precio de la Mano de Obra:")
    label_mano_obra.pack(pady=5)
    entry_mano_obra = ctk.CTkEntry(ventana, width=300)
    entry_mano_obra.pack(pady=5)

    # Campos para las medidas (ancho y largo)
    label_ancho = ctk.CTkLabel(ventana, text="Ancho (en metros):")
    label_ancho.pack(pady=5)
    entry_ancho = ctk.CTkEntry(ventana, width=300)
    entry_ancho.pack(pady=5)

    label_largo = ctk.CTkLabel(ventana, text="Largo (en metros):")
    label_largo.pack(pady=5)
    entry_largo = ctk.CTkEntry(ventana, width=300)
    entry_largo.pack(pady=5)

    
    def generar_pdf(nombre, telefono, total):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Presupuesto", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Cliente: {nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Teléfono: {telefono}", ln=True)
        pdf.cell(200, 10, txt=f"Total: ${total:.2f}", ln=True)

        pdf.output("presupuesto.pdf")
        messagebox.showinfo("Descarga completada", "El PDF se ha descargado exitosamente.")

    
    def calcular_presupuesto():
        try:
            nombre = entry_nombre.get()
            telefono = entry_telefono.get()
            precio_material = float(entry_precio.get())
            precio_mano_obra = float(entry_mano_obra.get())
            ancho = float(entry_ancho.get())
            largo = float(entry_largo.get())

            total =  precio_material * precio_mano_obra

            # Mostrar mensaje de exito
            messagebox.showinfo("Presupuesto generado", "Presupuesto generado exitosamente.")

            # Mostrar el boton de descarga
            boton_descargar = ctk.CTkButton(
                ventana,
                text="Descargar PDF",
                command=lambda: generar_pdf(nombre, telefono, total),
                fg_color="#005f73",
                hover_color="#0a9396",
                text_color="white"
            )
            boton_descargar.pack(pady=10)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores validos.")

    # Boton para calcular el presupuesto
    boton_calcular = ctk.CTkButton(
        ventana,
        text="Calcular Presupuesto",
        command=calcular_presupuesto,
        fg_color="#005f73",
        hover_color="#0a9396",
        text_color="white"
    )
    boton_calcular.pack(pady=10)
    
app.mainloop()
