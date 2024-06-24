import folium
import os
from pacientes import patients
import webview
import heapq
import geopandas as gpd
import requests
import polyline
from math import radians, sin, cos, sqrt, atan2

def show_map(coordenadas, direccion):
    # Función para obtener la ruta entre dos puntos utilizando la API de Directions de Google Maps
    def get_route(start, end, api_key):
        start = f"{start[0]},{start[1]}"
        end = f"{end[0]},{end[1]}"
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&key={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        route = data["routes"][0]["overview_polyline"]["points"]
        route = polyline.decode(route)
        return route

    # Coordenadas aproximadas de Lima, Perú
    lima_lat_range = (-12.05, -12.0)
    lima_lon_range = (-77.1, -77.0)

    # Crear el mapa centrado en Lima, Perú usando Folium
    mapa = folium.Map(location=[-12.0464, -77.0428], zoom_start=12)

    # Cargar los centros médicos de Lima desde el archivo GeoJSON
    geojson_path = "DB/export.geojson"  # Reemplaza con la ubicación de tu archivo GeoJSON
    centros_medicos = gpd.read_file(geojson_path)

    # Convertir las coordenadas de los centros médicos a una lista de tuplas
    centros_medicos_locations = [(coord[1], coord[0]) for coord in
                                centros_medicos.geometry.apply(lambda geom: geom.centroid.coords[:][0])]

    # Marcar todos los centros médicos en el mapa
    for center in centros_medicos_locations:
        folium.Marker(location=center, icon=folium.Icon(color='red')).add_to(mapa)

    # Convertir la lista de coordenadas del paciente en una tupla
    patient_node = tuple(coordenadas)

    # Marcar al paciente en el mapa
    folium.Marker(location=patient_node, icon=folium.Icon(color='orange')).add_to(mapa)

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

    # Algoritmo de Dijkstra para encontrar la ruta más corta entre dos puntos
    def dijkstra(graph, start, end):
        queue = [(0, start, [])]
        visited = set()
        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node not in visited:
                visited.add(node)
                path = path + [node]
                if node == end:
                    return cost, path
                for neighbor, edge_cost in graph.get(node, []):
                    if neighbor not in visited:
                        heapq.heappush(queue, (cost + edge_cost, neighbor, path))
        return float('inf'), []

    # Crear un grafo con las distancias calculadas usando Haversine
    graph = {}
    all_nodes = centros_medicos_locations + [patient_node]

    for i in range(len(all_nodes)):
        for j in range(i + 1, len(all_nodes)):
            distance = haversine(all_nodes[i], all_nodes[j])
            graph.setdefault(all_nodes[i], []).append((all_nodes[j], distance))
            graph.setdefault(all_nodes[j], []).append((all_nodes[i], distance))

    # Encontrar el centro médico más cercano al paciente
    min_distance = float('inf')
    closest_medical_center = None

    # Encontrar los 10 centros médicos más cercanos al paciente
    closest_medical_centers = heapq.nsmallest(10, centros_medicos_locations, key=lambda coord: haversine(patient_node, coord))

    # Pintar los 10 centros médicos más cercanos de color verde
    for center_coord in closest_medical_centers:
        folium.Marker(location=center_coord, icon=folium.Icon(color='green')).add_to(mapa)

    # Para cada paciente en la lista de pacientes por defecto
    for paciente in patients:
        # Obtener la ubicación del paciente
        patient_location = paciente.get_location()

        # Comprobar si patient_location es None
        if patient_location is not None:
            # Crear un marcador en la ubicación del paciente
            patient_marker = folium.Marker(location=patient_location,
                                        popup=folium.Popup(paciente.direccion, max_width=250),
                                        icon=folium.Icon(color='red'))

            # Añadir el marcador al mapa
            patient_marker.add_to(mapa)
        else:
            print(f"No se pudo obtener la ubicación para el paciente: {paciente.nombre}")

    # Función para calcular la distancia a lo largo de la ruta vehicular entre dos puntos
    def distance_along_route(start, end, route):
        total_distance = 0
        for i in range(len(route) - 1):
            segment_start = route[i]
            segment_end = route[i + 1]
            if segment_start == start:
                segment_distance = haversine(segment_start, end)
                total_distance += segment_distance
                break
            elif segment_end == start:
                break
            else:
                segment_distance = haversine(segment_start, segment_end)
                total_distance += segment_distance
        return total_distance

    # Encontrar el centro médico más cercano al paciente a lo largo de la ruta vehicular
    min_distance_along_route = float('inf')
    closest_medical_center_along_route = None

    for center_coord in closest_medical_centers:
        route = get_route(patient_node, center_coord, "AIzaSyDQJ5-AjJ8XixZmf7OiezCOOEfu4W4XSOc")
        if route:
            total_distance_along_route = distance_along_route(patient_node, center_coord, route)

            if total_distance_along_route < min_distance_along_route:
                min_distance_along_route = total_distance_along_route  # Corrección aquí
                closest_medical_center_along_route = center_coord

    # Encontrar los 2 centros médicos más cercanos al paciente
    closest_medical_centers = heapq.nsmallest(2, centros_medicos_locations, key=lambda coord: haversine(patient_node, coord))

    # Calcular la ruta desde el paciente hasta el centro médico más cercano a lo largo de la ruta vehicular utilizando la API de Directions de Google Maps
    if closest_medical_center_along_route:
        route = get_route(patient_node, closest_medical_center_along_route, "AIzaSyDQJ5-AjJ8XixZmf7OiezCOOEfu4W4XSOc")
        if route:
            folium.PolyLine(locations=route, color='purple').add_to(mapa)

    # Calcular la ruta desde el paciente hasta el primer centro médico más cercano utilizando la API de Directions de Google Maps
    if closest_medical_centers:
        route = get_route(patient_node, closest_medical_centers[0], "AIzaSyDQJ5-AjJ8XixZmf7OiezCOOEfu4W4XSOc")
        if route:
            folium.PolyLine(locations=route, color='purple').add_to(mapa)

    # Calcular la ruta desde el paciente hasta el segundo centro médico más cercano utilizando la API de Directions de Google Maps
    if len(closest_medical_centers) > 1:
        route = get_route(patient_node, closest_medical_centers[1], "AIzaSyDQJ5-AjJ8XixZmf7OiezCOOEfu4W4XSOc")
        if route:
            folium.PolyLine(locations=route, color='red').add_to(mapa)

    # Calcular la ruta desde el paciente hasta el centro médico más cercano utilizando la API de Directions de Google Maps
    if closest_medical_center:
        route = get_route(patient_node, closest_medical_center, "AIzaSyDQJ5-AjJ8XixZmf7OiezCOOEfu4W4XSOc")
        if route:
            folium.PolyLine(locations=route, color='green').add_to(mapa)

    # Marcar el centro médico más cercano al paciente en el mapa
    if closest_medical_center:
        folium.Marker(location=closest_medical_center, icon=folium.Icon(color='blue')).add_to(mapa)

    # Guardar el mapa en un archivo HTML
    mapa_path = os.path.join(os.getcwd(), "mapa_centros_medicos.html")
    mapa.save(mapa_path)

    # Verificar si el archivo HTML se creó correctamente
    if os.path.exists(mapa_path):
        print(f"El archivo {mapa_path} se ha creado correctamente.")
    else:
        print(f"Error: el archivo {mapa_path} no se ha creado.")

    # Abrir el archivo HTML en una ventana de navegador embebido
    webview.create_window("Mapa de centros médicos", mapa_path, width=800, height=600, resizable=True)
    webview.start()
