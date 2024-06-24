import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from MapaUbicacion import show_map

# Variables globales para almacenar coordenadas y dirección
coordenadas_globales = None
direccion_globales = None

ubicacion_entry = None  # Variable global para almacenar el Entry de la ubicación


def get_miubicacion_location():
    global ubicacion_entry

    def generar_mapa():
        global coordenadas_globales
        global direccion_globales

        # Obtener la ubicación ingresada
        ubicacion = ubicacion_entry.get()

        if ubicacion:
            if ',' in ubicacion:
                # Convertir la ubicación ingresada en una lista de coordenadas
                coordenadas = [float(coord.strip()) for coord in ubicacion.split(',')]
                if len(coordenadas) != 2:
                    showerror("Error", "Las coordenadas deben tener el formato 'latitud, longitud'.")
                    return

                # Mostrar las coordenadas en la consola
                print("Coordenadas guardadas:", coordenadas)
                # Llamar a la función importar de MapaUbicacion.py
                # Almacenar las coordenadas en la variable global
                coordenadas_globales = coordenadas
                # Limpiar la variable global de dirección
                direccion_globales = None
                # Llamar a la función importar para obtener las coordenadas del paciente


            else:
                # Mostrar la dirección en la consola
                print("Dirección guardada:", ubicacion)
                # Llamar a la función importar de MapaUbicacion.py
                # Almacenar la dirección en la variable global
                direccion_globales = ubicacion
                # Limpiar la variable global de coordenadas
                coordenadas_globales = None
                # Llamar a la función importar para obtener las coordenadas del paciente

            showerror("Ubicación Guardada", "La ubicación ha sido guardada correctamente.")
        else:
            showerror("Error", "Por favor ingrese una ubicación.")

    def ver_ubicacion():
        show_map(coordenadas_globales, direccion_globales)

    def ver_centro_medico():
        # Aquí iría la lógica para encontrar el centro médico más cercano
        pass

    root = tk.Tk()
    root.title("Mi Ubicación")

    # Crear el contenedor principal
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Etiqueta y campo de entrada para la ubicación con coordenadas
    ttk.Label(frame, text="Ingresa coordenadas (latitud, longitud):").grid(row=0, column=0, sticky=tk.W)
    ubicacion_entry = ttk.Entry(frame, width=30)
    ubicacion_entry.grid(row=1, column=0, padx=5, pady=5)

    # Botón "Guardar Ubicación" para coordenadas
    boton_guardar_coordenadas = ttk.Button(frame, text="Guardar Ubicación (Coordenadas)", command=generar_mapa)
    boton_guardar_coordenadas.grid(row=2, column=0, padx=10, pady=10)

    # Etiqueta y campo de entrada para la ubicación con dirección
    ttk.Label(frame, text="Ingresa una dirección:").grid(row=3, column=0, sticky=tk.W)
    direccion_entry = ttk.Entry(frame, width=30)
    direccion_entry.grid(row=4, column=0, padx=5, pady=5)

    # Botón "Guardar Ubicación" para dirección
    boton_guardar_direccion = ttk.Button(frame, text="Guardar Ubicación (Dirección)", command=generar_mapa)
    boton_guardar_direccion.grid(row=5, column=0, padx=10, pady=10)

    # Botón "Ver Ubicación"
    boton_ver_ubicacion = ttk.Button(frame, text="Ver Ubicación", command=ver_ubicacion)
    boton_ver_ubicacion.grid(row=6, column=0, padx=10, pady=10)

    # Botón "Ver Centro Médico Más Cercano"
    boton_ver_centro_medico = ttk.Button(frame, text="Ver Centro Médico Más Cercano", command=ver_centro_medico)
    boton_ver_centro_medico.grid(row=7, column=0, padx=10, pady=10)

    root.mainloop()


get_miubicacion_location()
