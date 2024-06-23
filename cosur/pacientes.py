import tkinter as tk
import os

def show_patient_screen():
    def open_map():
        os.system("python MapaFolium.py")  # Ejecutar MapaFolium.py al hacer clic en un paciente

    patient_window = tk.Toplevel()
    patient_window.title("Pacientes")
    patient_window.geometry("900x600")

    tk.Label(patient_window, text="Pacientes", font=("Helvetica", 32)).pack()

    # Crear un Listbox para mostrar la lista de pacientes
    patient_listbox = tk.Listbox(patient_window)
    patient_listbox.pack(fill="both", expand=True)

    # Añadir algunos pacientes de ejemplo al Listbox
    patients = ["Paciente 1", "Paciente 2", "Paciente 3"]
    for patient in patients:
        patient_listbox.insert(tk.END, patient)

    # Asociar la función open_map al evento de hacer clic en un paciente
    def on_patient_click(event):
        selected_patient_index = patient_listbox.curselection()
        if selected_patient_index:  # Verificar si se ha seleccionado un paciente
            open_map()

    patient_listbox.bind("<Double-Button-1>", on_patient_click)  # Evento de doble clic en un paciente


# Ejemplo de uso:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ejemplo")
    root.geometry("400x300")

    # Botón para mostrar la ventana de pacientes
    btn_show_patients = tk.Button(root, text="Mostrar Pacientes", command=show_patient_screen)
    btn_show_patients.pack()

    root.mainloop()