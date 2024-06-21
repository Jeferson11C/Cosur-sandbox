import tkinter as tk
from tkinter import ttk

def show_member_screen():
    # Crear una nueva ventana
    root = tk.Toplevel()

    root.title("Integrantes")
    root.geometry("600x300")
    root.configure(bg="gray")

    # Crear un marco para el Listbox
    frame = ttk.Frame(root, padding="10 10 10 10")
    frame.pack(fill="both", expand=True)

    # Crear un título para la ventana
    title = ttk.Label(frame, text="Integrantes", font=("Helvetica", 32), background="gray", foreground="white")
    title.pack(pady=(0, 40))

    # Crear un Listbox para mostrar la lista de integrantes
    member_listbox = tk.Listbox(frame, font=("Courier", 16), bg="white", fg="black", justify="center")
    member_listbox.pack(fill="both", expand=True)

    # Añadir algunos integrantes de ejemplo al Listbox
    members = ["Jeferson Smith Cabrera Camizan", "Bruce Andres Cipriano Chumbes", "Javier Tello Murga"]
    for member in members:
        member_listbox.insert(tk.END, member)