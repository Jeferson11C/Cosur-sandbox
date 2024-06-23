import webview
from geopy.geocoders import GoogleV3
import folium
import os
import requests
import geopandas as gpd
from math import radians, sin, cos, sqrt, atan2

def show_map(current_location, closest_medical_center, route):
    # Crear un mapa centrado en la ubicación actual
    mapa = folium.Map(location=current_location, zoom_start=14)

    # Marcar la ubicación actual del usuario
    folium.Marker(location=current_location, popup="Mi_ubicación", icon=folium.Icon(color='blue')).add_to(mapa)

    # Marcar el centro médico más cercano
    folium.Marker(location=closest_medical_center, popup="Centro Médico Más Cercano", icon=folium.Icon(color='red')).add_to(mapa)

    # Dibujar la ruta
    folium.PolyLine(locations=route, color='green').add_to(mapa)

    # Guardar el mapa en un archivo HTML
    mapa_path = os.path.join(os.getcwd(), "mapa_mi_ubicacion.html")
    mapa.save(mapa_path)

    # Abrir el archivo HTML en una ventana de navegador embebido
    webview.create_window("Mapa de mi ubicación", mapa_path, width=800, height=600, resizable=True)
    webview.start()

def get_route(api_key, origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin[0]},{origin[1]}&destination={destination[0]},{destination[1]}&key={api_key}"
    response = requests.get(url)
    directions = response.json()

    if directions["status"] == "OK":
        route = []
        for step in directions["routes"][0]["legs"][0]["steps"]:
            lat = step["end_location"]["lat"]
            lon = step["end_location"]["lng"]
            route.append((lat, lon))
        return route
    else:
        print("Error en la obtención de la ruta:", directions["status"])
        return []

def show_current_location(api_key, geojson_path):
    # Crear un geocodificador con la clave API de Google Maps
    geolocator = GoogleV3(api_key=api_key)

    # Aquí necesitas una manera válida de obtener la ubicación actual.
    # Por simplicidad, usaremos una ubicación fija.
    location = geolocator.geocode("callao,estaciom_bayovar")  # Reemplaza con una ubicación válida o con un método para obtener la ubicación actual

    # Verificar si geolocator pudo obtener la ubicación
    if location is None:
        print("No se pudo obtener la ubicación.")
        return None

    # Coordenadas de la ubicación actual
    current_location = [location.latitude, location.longitude]

    # Cargar los centros médicos de Lima desde el archivo GeoJSON
    centros_medicos = gpd.read_file(geojson_path)

    # Convertir las coordenadas de los centros médicos a una lista de tuplas
    centros_medicos_locations = [(coord[1], coord[0]) for coord in
                                 centros_medicos.geometry.apply(lambda geom: geom.centroid.coords[:][0])]

    # Encontrar el centro médico más cercano
    min_distance = float('inf')
    closest_medical_center = None

    for center in centros_medicos_locations:
        distance = haversine(current_location, center)
        if distance < min_distance:
            min_distance = distance
            closest_medical_center = center

    # Obtener la ruta más corta desde la ubicación actual hasta el centro médico más cercano
    if closest_medical_center:
        route = get_route(api_key, current_location, closest_medical_center)
        show_map(current_location, closest_medical_center, route)

    return current_location

# Función de Haversine para calcular la distancia entre dos puntos geográficos
def haversine(coord1, coord2):
    R = 6371  # Radio de la Tierra en kilómetros
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

if __name__ == "__main__":
    API_KEY = "AIzaSyDQJ5-AjJ8XixZmf7OiezCOOEfu4W4XSOc"
    GEOJSON_PATH = "DB/export.geojson"
    show_current_location(API_KEY, GEOJSON_PATH)
