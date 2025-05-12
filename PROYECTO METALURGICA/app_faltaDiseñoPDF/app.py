from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkToplevel,CTkFrame,CTkCheckBox,CTkImage,set_appearance_mode,get_appearance_mode
import webbrowser
from tkinter import messagebox
from fpdfGenerador import generar_pdf
import os
from PIL import Image
color_boton= "#FFD51E" 
color_fondo="#201E1E" 
color_hover = "#8C7204"
imagenn = Image.open(os.path.join(os.path.dirname(__file__), 'tema.png'))
imagen_tema = CTkImage(imagenn,size=(50, 50))

class ReciboFactura:
    def __init__(self, root):
        self.__root = root
        self.__root.configure()
        self.__root.title("Recibo de Factura")
        ancho_ventana = 600
        alto_ventana = 650
        root.iconbitmap(os.path.join(os.path.dirname(__file__), 'logo_monocromatico.ico'))
        
        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.__root.winfo_screenwidth()
        alto_pantalla = self.__root.winfo_screenheight()
        set_appearance_mode("dark")  # Modo claro/oscuro
        # Calcular coordenadas para centrar
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))

        self.__root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Frame principal para navegación
        self.frame_nav = CTkFrame(root, bg_color="transparent", height=60)
        self.frame_nav.pack(pady=10)

        # Frames de contenido
        self.frame_inicio = CTkFrame(root)
        self.frame_recibo = CTkFrame(root)
        self.frame_presupuesto = CTkFrame(root)

        # Mostrar primero el frame de inicio
        self.mostrar_frame(self.frame_inicio)

        # Botones de navegación
        CTkButton(self.frame_nav, text="Inicio",text_color="black",hover_color=color_hover, command=lambda: self.mostrar_frame(self.frame_inicio),fg_color=color_boton).pack(side="left", padx=5)
        
        CTkButton(self.frame_nav, text="Presupuesto",hover_color=color_hover,text_color="black", command=lambda: self.mostrar_frame(self.frame_presupuesto),fg_color=color_boton).pack(side="left", padx=5)
        
        CTkButton(self.frame_nav, text="Generar Recibo en ARCA",hover_color=color_hover,text_color="black",fg_color=color_boton, command=lambda: webbrowser.open("https://www.arca.gob.ar/fe/")).pack(side="left", padx=5)
        
        CTkButton(self.frame_nav, text="",image=imagen_tema,fg_color="transparent", command=lambda: self.cambiar()).pack(side="left", padx=5)
    def cambiar(self):
        if get_appearance_mode() == "Light":
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")
    
        # Contenido del frame de inicio
        imagen = Image.open(os.path.join(os.path.dirname(__file__), 'fondoapp.png'))
        imagen_ctk = CTkImage(light_image=imagen,dark_image=imagen,size=(600, 620))
        CTkLabel(self.frame_inicio, image=imagen_ctk,text="" ).pack(ipady=0.5)

        # Contenido del frame de presupuesto
        self.campos = {}
        for campo in ["Nombre del Cliente", "Numero de Teléfono", "Precio del Material", "Precio de la Mano de Obra", "Ancho (en metros)", "Largo (en metros)"]:
            CTkLabel(self.frame_presupuesto, text=campo + ":").pack(pady=5)
            entrada = CTkEntry(self.frame_presupuesto, width=300)
            entrada.pack(pady=5)
            self.campos[campo] = entrada
        self.opcion_aluminio = CTkCheckBox(self.frame_presupuesto, text="Persiana de Aluminio",fg_color=color_boton)
        self.opcion_aluminio.pack(pady=5)
        self.opcion_metalica = CTkCheckBox(self.frame_presupuesto, text="Persiana Metalica",fg_color=color_boton)
        self.opcion_metalica.pack(pady=5)
        CTkButton(self.frame_presupuesto,hover_color=color_hover,text_color="black",fg_color=color_boton, text="Calcular Presupuesto", command=lambda: self.calcular_presupuesto()).pack(pady=10)
        
    
            
    def calcular_presupuesto(self):
        try:
            nombre = self.campos["Nombre del Cliente"].get()
            telefono = self.campos["Numero de Teléfono"].get()
            precio_material = float(self.campos["Precio del Material"].get())
            precio_mano_obra = float(self.campos["Precio de la Mano de Obra"].get())
            ancho = float(self.campos["Ancho (en metros)"].get())
            largo = float(self.campos["Largo (en metros)"].get())

            total = precio_material * precio_mano_obra
            if self.opcion_aluminio.get() and self.opcion_metalica.get():
                messagebox.showerror("Error", "Seleccione solo una opción de persiana.")
                return
            elif self.opcion_aluminio.get():
                    tipo_persiana = "Aluminio"
            elif self.opcion_metalica.get():
                    tipo_persiana = "Metalica"
            else:
                    messagebox.showerror("Error", "Seleccione un tipo de persiana.")
                    return

            generar_pdf(nombre, telefono, total,tipo_persiana)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

    def persianas_metalicas(self):
        self.ventana_presupuesto("Persianas Metálicas")

    def persianas_aluminio(self):
        self.ventana_presupuesto("Persianas de Aluminio")

    def mostrar_frame(self, frame_a_mostrar):
        # Oculta todos los frames
        for frame in [self.frame_inicio, self.frame_presupuesto]:
            frame.pack_forget()
        # Muestra el que corresponde
        frame_a_mostrar.pack(fill="both", expand=True)

    
