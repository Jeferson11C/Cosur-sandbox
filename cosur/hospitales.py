import tkinter as tk

def show_hospital_screen():
    patient_window = tk.Toplevel()
    patient_window.title("Hospitales")
    patient_window.geometry("900x600")

    tk.Label(patient_window, text="Hospitales", font=("Helvetica", 32)).pack()

    # Crear un Listbox para mostrar la lista de pacientes
    patient_listbox = tk.Listbox(patient_window)
    patient_listbox.pack(fill="both", expand=True)

    # Añadir algunos pacientes de ejemplo al Listbox
    patients = ["Hospital 1", "Hospital 2", "Hospital 3"]
    for patient in patients:
        patient_listbox.insert(tk.END, patient)