import tkinter as tk
import os

def show_hospital_screen():
    def open_map():
        os.system("python MapaFolium.py")  # Ejecutar MapaFolium.py al hacer clic en un hospital

    hospital_window = tk.Toplevel()
    hospital_window.title("Hospitales")
    hospital_window.geometry("900x600")

    tk.Label(hospital_window, text="Hospitales", font=("Helvetica", 32)).pack()

    # Crear un Listbox para mostrar la lista de hospitales
    hospital_listbox = tk.Listbox(hospital_window)
    hospital_listbox.pack(fill="both", expand=True)

    # Añadir algunos hospitales de ejemplo al Listbox
    hospitals = ["Hospital 1", "Hospital 2", "Hospital 3"]
    for hospital in hospitals:
        hospital_listbox.insert(tk.END, hospital)

    # Asociar la función open_map al evento de hacer clic en un hospital
    def on_hospital_click(event):
        selected_hospital_index = hospital_listbox.curselection()
        if selected_hospital_index:  # Verificar si se ha seleccionado un hospital
            open_map()

    hospital_listbox.bind("<Double-Button-1>", on_hospital_click)  # Evento de doble clic en un hospital



# Ejemplo de uso:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ejemplo")
    root.geometry("400x300")

    # Botón para mostrar la ventana de hospitales
    btn_show_hospitals = tk.Button(root, text="Mostrar Hospitales", command=show_hospital_screen)
    btn_show_hospitals.pack()

    root.mainloop()
