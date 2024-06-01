import tkinter as tk
from tkinter import ttk

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
        self.canvas.create_image(0, 0, image=self.logo_image, anchor="nw")

        # titulo
        self.canvas.create_text(180, 40, text="COSUR", font=("Helvetica", 32), fill="red")

        self.create_button(self.canvas, "Navegar al paciente", 0)
        self.create_button(self.canvas, "Navegar al hospital", 1)

    def create_button(self, parent, text, row):
        button = ttk.Button(parent, text=text, style="Content.TButton")
        button.place(x=50, y=150 + row * 60)


# Application setup
root = tk.Tk()

# Define styles
style = ttk.Style()
style.configure("Content.TFrame", background="transparent")
style.configure("Content.TButton", font=("Helvetica", 14), anchor="center", background="red", relief="flat")

# Create and place the custom card
card = CosurCard(root)
card.pack(fill="both", expand=True, pady=20, padx=20)

# Run
root.mainloop()