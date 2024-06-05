import folium
import os
import webview

# Crear el mapa centrado en Perú usando Folium
mapa = folium.Map(location=[-9.19, -75.0152], zoom_start=6)

# Guardar el mapa en un archivo HTML
mapa_path = os.path.join(os.getcwd(), "mapa_peru.html")
mapa.save(mapa_path)

# Verificar si el archivo HTML se creó correctamente
if os.path.exists(mapa_path):
    print(f"El archivo {mapa_path} se ha creado correctamente.")
else:
    print(f"Error: el archivo {mapa_path} no se ha creado.")

# Abrir el archivo HTML en una ventana de navegador embebido
webview.create_window("Mapa de Perú", mapa_path, width=800, height=600, resizable=True)
webview.start()
