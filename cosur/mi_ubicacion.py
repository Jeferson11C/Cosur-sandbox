import webview
from geopy.geocoders import GoogleV3
import folium
import os

def show_map(current_location):
    # Crear un mapa centrado en la ubicación actual
    mapa = folium.Map(location=current_location, zoom_start=14)

    # Aquí va el código de MapaFolium.py que genera el mapa
    # Asegúrate de reemplazar las referencias a 'patient_node' con la ubicación actual del usuario
    # ...

    # Guardar el mapa en un archivo HTML
    mapa_path = os.path.join(os.getcwd(), "mapa_mi_ubicacion.html")
    mapa.save(mapa_path)

    # Abrir el archivo HTML en una ventana de navegador embebido
    webview.create_window("Mapa de mi ubicación", mapa_path, width=800, height=600, resizable=True)
    webview.start()

def show_current_location():
    # Crear un geocodificador con la clave API de Google Maps
    geolocator = GoogleV3(api_key="AIzaSyDQJ5-AjJ8XixZmf7OiezCOOEfu4W4XSOc")

    # Obtener la ubicación actual
    location = geolocator.geocode("mi ubicación actual")

    # Verificar si geolocator pudo obtener la ubicación
    if location is None:
        print("No se pudo obtener la ubicación.")
        return None

    # Devolver las coordenadas de la ubicación actual
    current_location = [location.latitude, location.longitude]

    # Mostrar el mapa cuando el usuario haga clic en su ubicación
    show_map(current_location)

    return current_location