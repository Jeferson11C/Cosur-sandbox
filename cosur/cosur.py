import tkinter as tk
from tkinter import ttk
from pacientes import show_patient_screen
from hospitales import show_hospital_screen
from creditos import show_member_screen
from ubicacion import get_miubicacion_location

class CosurCard(ttk.Frame):

    def __init__(self, ventana):
        super().__init__(ventana)
        self.ventana = ventana
        self.ventana.title("COSUR")
        self.ventana.geometry("900x600")
        self.ventana.configure(bg="gray")
        self.configure(style="Card.TFrame")

        # fondo de la card
        self.background_image = tk.PhotoImage(file="imagenes/fondo (1).png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=900, height=600, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Colocar el logo
        self.logo_image = tk.PhotoImage(file="imagenes/logo.png")
        self.logo_image = self.logo_image.subsample(7)
        self.canvas.create_image(10, 10, image=self.logo_image, anchor="nw")

        # Título
        self.canvas.create_text(120, 50, text="COSUR", font=("Helvetica", 32, "bold"), fill="red", anchor="w")

        # Agregar textos informativos a la derecha
        self.canvas.create_text(750, 100, text="¡Salvando Vidas con Eficiencia!", font=("Helvetica", 18, "bold"), fill="black", anchor="e")
        self.canvas.create_text(750, 150, text="Navega rápidamente a pacientes y hospitales\ncon nuestro sistema de rutas optimizadas.", font=("Helvetica", 14), fill="black", anchor="e")
        self.canvas.create_text(750, 220, text="Rutas optimizadas en tiempo real.\nAsignación rápida y precisa de ambulancias.\nMonitoreo en vivo y actualizaciones instantáneas.", font=("Helvetica", 12), fill="black", justify="right", anchor="e")
        self.canvas.create_text(750, 300, text="Comienza ahora y reduce los tiempos de respuesta.", font=("Helvetica", 14, "bold"), fill="black", anchor="e")

        # Crear botones
        self.create_button(self.canvas, "Navegar al paciente", 0)
        self.create_button(self.canvas, "Navegar al hospital", 1)
        self.create_button(self.canvas, "Creditos", 2)
        self.create_button(self.canvas, "Mi ubicación", 3)



    def create_button(self, parent, text, row):
        try:
            if text == "Navegar al paciente":
                button = ttk.Button(parent, text=text, style="Content.TButton", command=show_patient_screen)
                button.place(x=50, y=150 + row * 60)
            elif text == "Navegar al hospital":
                button = ttk.Button(parent, text=text, style="Content.TButton", command=show_hospital_screen)
                button.place(x=50, y=150 + row * 60)
            elif text == "Mi ubicación":
                button = ttk.Button(parent, text=text, style="Content.TButton", command=get_miubicacion_location)
                button.place(x=50, y=150 + row * 60 )
            elif text == "Creditos":
                button = ttk.Button(parent, text=text, style="Content.TButton", command=show_member_screen)
                button.place(x=50, y=350 + row * 60)
        except Exception as e:
            print(f"Error: {e}")

# Configuración de la aplicación
root = tk.Tk()

# Definir estilos
style = ttk.Style()
style.configure("Content.TFrame", background="transparent")
style.configure("Content.TButton", font=("Helvetica", 14), anchor="center", background="red", relief="flat")

# Crear y colocar la tarjeta personalizada
card = CosurCard(root)
card.pack(fill="both", expand=True, pady=20, padx=20)

# Ejecutar la aplicación
root.mainloop()