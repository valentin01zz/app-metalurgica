import customtkinter as ctk
import tkinter as tk
import requests
import csv
import time
import webbrowser

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
        with open("pruebas\materiales.csv",newline='',encoding='utf-8') as archivo_csv: 
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
app.title("Generador de Boletas Estéticas")
app.state('zoomed')
def ventana_recibo():
    ventana = ctk.CTkToplevel(app)
    ventana.title("Recibo")
    ventana.geometry("500x500")
    ventana.resizable(False,False)
    ventana.transient(app)  # Hace que esta ventana dependa de la que pongaen ()
    ventana.grab_set() # # Hace que la ventana sea modal y no se pueda interactuar con la ventana principal hasta que se cierre
    label_dolar = ctk.CTkLabel(ventana,text=f"Compra: {compra}\nVenta: {venta}",text_color="black",font=("Arial",20),fg_color="#2F1205")
    label_dolar.pack(side="left")
button_recibo = ctk.CTkButton(app,text="Recibo",command=ventana_recibo,fg_color="#000000",hover_color="lightgray",text_color="red")
button_factura = ctk.CTkButton(app,text="Factura",command= abrir_web_factura)
button_recibo.pack()
button_factura.pack()
app.mainloop()










