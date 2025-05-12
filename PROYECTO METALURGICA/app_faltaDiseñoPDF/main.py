import customtkinter as ctk
from app import ReciboFactura
if __name__ == "__main__":
    app = ctk.CTk()
    ReciboFactura(app)
    app.mainloop()