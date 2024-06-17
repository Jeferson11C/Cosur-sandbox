import folium
import os
import webview
import random
import heapq
import geopandas as gpd

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


# Algoritmo de Dijkstra para encontrar la ruta más corta entre dos puntos
def dijkstra(edges, start, end):
    graph = {}
    for edge in edges:
        src, dest, weight = edge
        if src not in graph:
            graph[src] = []
        if dest not in graph:
            graph[dest] = []
        graph[src].append((dest, weight))
        graph[dest].append((src, weight))


    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [node]

            if node == end:
                return cost, path

            for neighbor, edge_cost in graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + edge_cost, neighbor, path))

    return float('inf'), None

# Crear nodo de paciente (amarillo) en Lima, Perú
patient_node = (random.uniform(lima_lat_range[0], lima_lat_range[1]),
                random.uniform(lima_lon_range[0], lima_lon_range[1]))  # Coordenadas aleatorias dentro de Lima

# Encontrar el centro médico más cercano al paciente
min_distance = float('inf')
closest_medical_center = None
for center in centros_medicos_locations:
    distance, _ = dijkstra([(patient_node, center, 1)], patient_node, center)
    if distance < min_distance:
        min_distance = distance
        closest_medical_center = center

# Marcar el centro médico más cercano al paciente en el mapa
if closest_medical_center:
    folium.Marker(location=closest_medical_center, icon=folium.Icon(color='blue')).add_to(mapa)

# Calcular la ruta más corta desde el paciente hasta el centro médico más cercano
if closest_medical_center:
    _, path = dijkstra([(patient_node, closest_medical_center, 1)], patient_node, closest_medical_center)
    if path:
        folium.PolyLine(locations=path, color='green').add_to(mapa)

# Marcar al paciente en el mapa
folium.Marker(location=patient_node, icon=folium.Icon(color='yellow')).add_to(mapa)

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
