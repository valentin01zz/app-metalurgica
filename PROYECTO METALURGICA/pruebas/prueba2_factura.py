import customtkinter as ctk
import tkinter as tk
import csv
app = ctk.CTk()
app.title("Generador de Boletas Estéticas")
app.state('zoomed')
app.resizable(False,False)
class gestor_materiales():
    __materiales: float
    def __init__(self):
        self.__materiales = 0
    def set_precio(self, precio):
        self.__materiales = precio
    def cargar_materiales(self):
        with open("pruebas\materiales.csv",newline='',encoding='utf-8') as archivo_csv: 
            reader = csv.reader(archivo_csv,delimiter=';') 
            next(reader)
            for fila in reader: 
                self.set_precio(float(fila[0]))
                break
            print(self.__materiales)
   
GM = gestor_materiales()
GM.cargar_materiales()
app.mainloop()