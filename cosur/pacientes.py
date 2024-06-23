import tkinter as tk
import os
from geopy.geocoders import GoogleV3

class Paciente:
    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion

    def get_location(self):
        geolocator = GoogleV3(api_key="AIzaSyDQJ5-AjJ8XixZmf7OiezCOOEfu4W4XSOc")
        try:
            location = geolocator.geocode(self.direccion)
            if location is None:
                print(f"No se pudo obtener la ubicación para la dirección: {self.direccion}")
                return None
            return [location.latitude, location.longitude]
        except Exception as e:
            print(f"Error al obtener la ubicación para la dirección: {self.direccion}. Error: {e}")
            return None

# Crear una lista global de pacientes
# Crear una lista global de pacientes con direcciones específicas en Lima
patients = [
    Paciente("Paciente 1", "Av. Javier Prado Este 4200, Lima 15023, Perú"),
    Paciente("Paciente 2", "Av. Alfredo Mendiola 1400, Independencia 15311, Perú"),
    Paciente("Paciente 3", "Av. La Marina 2000, San Miguel 15087, Perú")
]

def show_patient_screen():
    def open_map(patient):
        os.system( f"python MapaFolium.py {patient.nombre} {patient.direccion}")  # Ejecutar MapaFolium.py al hacer clic en un paciente# Ejecutar MapaFolium.py al hacer clic en un paciente # Ejecutar MapaFolium.py al hacer clic en un paciente

    patient_window = tk.Toplevel()
    patient_window.title("Pacientes")
    patient_window.geometry("900x600")

    tk.Label(patient_window, text="Pacientes", font=("Helvetica", 32)).pack()

    # Crear campos de entrada para el nombre y la dirección del paciente
    patient_name_entry = tk.Entry(patient_window)
    patient_name_entry.pack()
    patient_address_entry = tk.Entry(patient_window)
    patient_address_entry.pack()

    # Crear un Listbox para mostrar la lista de pacientes
    patient_listbox = tk.Listbox(patient_window)
    patient_listbox.pack(fill="both", expand=True)


    for patient in patients:
        patient_listbox.insert(tk.END, patient.nombre)


    # Asociar la función open_map al evento de hacer clic en un paciente
    def on_patient_click(event):
        selected_patient_index = patient_listbox.curselection()
        if selected_patient_index:  # Verificar si se ha seleccionado un paciente
            if selected_patient_index[0] < len(patients):  # Check if the index is within the range of the list
                selected_patient = patients[selected_patient_index[0]]  # Obtener el paciente seleccionado
                open_map(selected_patient)  # Pasar el paciente seleccionado a la función open_map
            else:
                print("Selected index is out of range")
        else:
            print("No patient selected")

    patient_listbox.bind('<Double-1>', on_patient_click)  # Conectar la función `on_patient_click` al evento de doble clic en la lista de pacientes en la GUI # Evento de doble clic en un paciente

    # Función para crear un nuevo paciente y añadirlo a la lista de pacientes
    def create_patient():
        patient_name = patient_name_entry.get()
        patient_address = patient_address_entry.get()
        new_patient = Paciente(patient_name, patient_address)  # Crear un nuevo paciente
        patients.append(new_patient)  # Agregar el nuevo paciente a la lista `patients`
        patient_listbox.insert(tk.END,
                               patient_name)  # Agregar el nombre del nuevo paciente a la lista de pacientes en la GUI



    def add_patient(name, address):
        new_patient = Paciente(name, address)  # Crear un nuevo paciente
        patients.append(new_patient)  # Agregar el nuevo paciente a la lista `patients`


    # Botón para crear un nuevo paciente
    create_patient_button = tk.Button(patient_window, text="Crear", command=create_patient)
    create_patient_button.pack()


# Ejemplo de uso:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ejemplo")
    root.geometry("400x300")

    # Botón para mostrar la ventana de pacientes
    btn_show_patients = tk.Button(root, text="Mostrar Pacientes", command=show_patient_screen)
    btn_show_patients.pack()

    root.mainloop()

