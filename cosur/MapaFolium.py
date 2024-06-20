import folium
import os
import webview
import random
import heapq
import geopandas as gpd
from math import radians, sin, cos, sqrt, atan2

# Coordenadas aproximadas de Lima, Perú
lima_lat_range = (-12.05, -12.0)  # Ajuste para asegurar que esté dentro de la ciudad
lima_lon_range = (-77.1, -77.0)  # Ajuste para asegurar que esté dentro de la ciudad

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

# Crear nodo de paciente (amarillo) en Lima, Perú
patient_node = (random.uniform(lima_lat_range[0], lima_lat_range[1]),
                random.uniform(lima_lon_range[0], lima_lon_range[1]))  # Coordenadas aleatorias dentro de Lima

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

for center in centros_medicos_locations:
    distance, _ = dijkstra(graph, patient_node, center)
    if distance < min_distance:
        min_distance = distance
        closest_medical_center = center

# Calcular la ruta más corta desde el paciente hasta el centro médico más cercano
if closest_medical_center:
    _, path = dijkstra(graph, patient_node, closest_medical_center)
    if path:
        folium.PolyLine(locations=path, color='green').add_to(mapa)

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
