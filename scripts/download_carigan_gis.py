import os
import sys
import json
import requests
from pathlib import Path

def download_carigan_gis():
    print("Iniciando descarga de datos geográficos oficiales enriquecidos para Carigán (Macro y Micro)...")
    
    # 1. Definir rutas en el Data Lake Centralizado (~/.capital/lake/)
    lake_dir = Path.home() / ".capital" / "lake" / "datasets"
    lake_dir.mkdir(parents=True, exist_ok=True)
    lake_file = lake_dir / "carigan_boundary.geojson"
    
    # 2. Ruta local en el repositorio de proyectos
    local_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
    local_dir.mkdir(parents=True, exist_ok=True)
    local_link = local_dir / "carigan_boundary.geojson"
    
    # 3. Consulta a la API de Overpass (OpenStreetMap) para límites, vías e hidrografía
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Bounding box acotado a nivel macro [-4.06, -79.28, -3.92, -79.15]
    query = """
    [out:json][timeout:90];
    (
      // Capa Local Carigán (Detalle Completo de calles, caminos y ríos)
      way["highway"](-4.00, -79.23, -3.96, -79.19);
      way["waterway"](-4.00, -79.23, -3.96, -79.19);
      
      // Capa Macro Loja (Vías principales, troncales estatales y ríos mayores para conectividad regional)
      way["highway"~"primary|secondary|tertiary|trunk"](-4.06, -79.28, -3.92, -79.15);
      way["waterway"~"river"](-4.06, -79.28, -3.92, -79.15);
      
      // Límites administrativos parroquiales y cantonales de todo el cuadrante norte y centro
      relation["boundary"="administrative"](-4.06, -79.28, -3.92, -79.15);
      way["boundary"="administrative"](-4.06, -79.28, -3.92, -79.15);
    );
    out body;
    >;
    out skel qt;
    """
    
    try:
        print("Enviando petición multiescala enriquecida a Overpass API...")
        headers = {
            "User-Agent": "UNL_Economic_Research_Bot/1.0 (condoyerick99@gmail.com)"
        }
        response = requests.post(overpass_url, data={"data": query}, headers=headers, timeout=90)
        response.raise_for_status()
        data = response.json()
        
        elements = data.get("elements", [])
        print(f"Petición completada con éxito. Elementos descargados: {len(elements)}")
        
        # 4. Procesar y estructurar en GeoJSON
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        nodes = {el["id"]: el for el in elements if el["type"] == "node"}
        ways = [el for el in elements if el["type"] == "way"]
        
        print("Modelando geometrías LineString a partir de nodos...")
        for way in ways:
            coordinates = []
            for node_id in way.get("nodes", []):
                if node_id in nodes:
                    node = nodes[node_id]
                    coordinates.append([node["lon"], node["lat"]])
                    
            if len(coordinates) > 1:
                # Conservamos el elemento si entra dentro de nuestro marco macro
                is_macro = any(
                    -79.285 < pt[0] < -79.145 and -4.065 < pt[1] < -3.915 
                    for pt in coordinates
                )
                
                if is_macro:
                    feature = {
                        "type": "Feature",
                        "properties": way.get("tags", {}),
                        "geometry": {
                            "type": "LineString",
                            "coordinates": coordinates
                        }
                    }
                    geojson["features"].append(feature)
                    
        # Guardar puntos de interés
        for el in elements:
            if el["type"] == "node" and "tags" in el:
                lon, lat = el["lon"], el["lat"]
                if -79.28 < lon < -79.15 and -4.06 < lat < -3.92:
                    feature = {
                        "type": "Feature",
                        "properties": el["tags"],
                        "geometry": {
                            "type": "Point",
                            "coordinates": [lon, lat]
                        }
                    }
                    geojson["features"].append(feature)
                    
        print(f"GeoJSON multiescala estructurado con {len(geojson['features'])} entidades locales y regionales.")
        
        # Guardar en el Data Lake centralizado
        print(f"Guardando archivo en el Data Lake centralizado: {lake_file}")
        with open(lake_file, "w", encoding="utf-8") as f:
            json.dump(geojson, f, indent=2, ensure_ascii=False)
            
        # 5. Crear enlace simbólico
        if local_link.exists() or local_link.is_symlink():
            local_link.unlink()
            
        local_link.symlink_to(lake_file)
        print("¡Proceso de sincronización GIS completado con éxito!")
        return True
        
    except Exception as e:
        print(f"Error durante el proceso: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    download_carigan_gis()
