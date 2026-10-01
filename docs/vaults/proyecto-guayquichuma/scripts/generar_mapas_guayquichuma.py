import urllib.request
import json
import os
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import shape

vault_dir = 'd:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-guayquichuma'
asset_dir = f'{vault_dir}/asset'
os.makedirs(asset_dir, exist_ok=True)

headers = {'User-Agent': 'UNL-Economia-Project-Guayquichuma/1.0'}

def fetch_geojson(query):
    url = f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&polygon_geojson=1'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode())
        for item in res:
            if 'geojson' in item and item['geojson']['type'] in ['Polygon', 'MultiPolygon']:
                return item
    return None

print("Descargando polígonos...")
guay = fetch_geojson('Guayquichuma, Catamayo, Loja, Ecuador')
catamayo = fetch_geojson('Catamayo, Loja, Ecuador')

geom_guay = shape(guay['geojson']) if guay else None
geom_cat = shape(catamayo['geojson']) if catamayo else None

gdf_cat = gpd.GeoDataFrame([{'name': 'Cantón Catamayo', 'geometry': geom_cat}], crs='EPSG:4326') if geom_cat else None
gdf_guay = gpd.GeoDataFrame([{'name': 'Parroquia Guayquichuma', 'geometry': geom_guay}], crs='EPSG:4326') if geom_guay else None

# ----------------- MAPA 1: Macro-localización Cantonal -----------------
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

if gdf_cat is not None:
    gdf_cat.plot(ax=ax, color='#e8f8f5', edgecolor='#16a085', linewidth=1.5, label='Cantón Catamayo')
if gdf_guay is not None:
    gdf_guay.plot(ax=ax, color='#fdebd0', edgecolor='#d35400', linewidth=2.0, label='Parroquia Guayquichuma (10.584,10 ha)')

# Puntos clave cantonales
puntos_macro = [
    ('Cabecera Guayquichuma', -79.5514, -3.8772, '#c0392b'),
    ('Catamayo (Cabecera Cantonal)', -79.3582, -3.9875, '#2980b9'),
    ('Zambi', -79.5100, -3.9400, '#7f8c8d'),
    ('San Pedro de la Bendita', -79.4200, -3.9500, '#7f8c8d')
]

for label, lon, lat, col in puntos_macro:
    ax.plot(lon, lat, marker='o', color=col, markersize=5 if 'Catamayo' in label else 4)
    offset_x = 0.015 if 'Catamayo' in label else 0.01
    ax.text(lon + offset_x, lat, label, fontsize=6.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85, edgecolor=col, linewidth=0.6))

# Acotar límites a la extensión cantonal
minx, miny, maxx, maxy = geom_cat.bounds
pad_x = (maxx - minx) * 0.08
pad_y = (maxy - miny) * 0.08
ax.set_xlim(minx - pad_x, maxx + pad_x)
ax.set_ylim(miny - pad_y, maxy + pad_y)

ax.set_title("Contextualización de Guayquichuma en el Cantón Catamayo", fontsize=8.5, fontweight='bold', pad=10)
ax.set_xlabel("Longitud (WGS84)", fontsize=7.5)
ax.set_ylabel("Latitud (WGS84)", fontsize=7.5)
ax.grid(True, linestyle='--', alpha=0.4, color='#bdc3c7')

plt.tight_layout()
plt.savefig(f'{asset_dir}/mapa_macro_guayquichuma.png', dpi=300)
plt.close()
print("Mapa macro perfeccionado.")

# ----------------- MAPA 2: Micro-localización Parroquial -----------------
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

if gdf_guay is not None:
    gdf_guay.plot(ax=ax, color='#f4fbf7', edgecolor='#1e8449', linewidth=2.0)

# Asentamientos
barrios = [
    ('Cabecera Parroquial', -79.5514, -3.8772, '#922b21'),
    ('Chiguango Alto', -79.5420, -3.8650, '#2874a6'),
    ('Chiguango Bajo', -79.5480, -3.8710, '#2874a6'),
    ('El Tambo', -79.5620, -3.8850, '#2874a6'),
    ('La Primavera', -79.5580, -3.8920, '#2874a6'),
    ('Rumipotrero', -79.5350, -3.8800, '#2874a6'),
    ('Santa Ana', -79.5680, -3.8600, '#2874a6')
]

for name, lon, lat, col in barrios:
    ax.plot(lon, lat, marker='s' if 'Cabecera' in name else 'o', color=col, markersize=6 if 'Cabecera' in name else 4)
    ax.text(lon + 0.003, lat + 0.001, name, fontsize=6.5, 
            fontweight='bold' if 'Cabecera' in name else 'normal',
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', alpha=0.9, edgecolor=col, linewidth=0.5))

ax.text(0.04, 0.90, "Área de Conservación Municipal ACMUS (7.092,80 ha)\nZona Intangible y APH San Pedro - Zambi - Guayquichuma", 
        transform=ax.transAxes, fontsize=7, fontstyle='italic',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#d5f5e3', edgecolor='#27ae60', alpha=0.9))

minx, miny, maxx, maxy = geom_guay.bounds
pad_x = (maxx - minx) * 0.05
pad_y = (maxy - miny) * 0.05
ax.set_xlim(minx - pad_x, maxx + pad_x)
ax.set_ylim(miny - pad_y, maxy + pad_y)

ax.set_title("Asentamientos Humanos y Núcleos Rurales de Guayquichuma", fontsize=8.5, fontweight='bold', pad=10)
ax.set_xlabel("Longitud (WGS84)", fontsize=7.5)
ax.set_ylabel("Latitud (WGS84)", fontsize=7.5)
ax.grid(True, linestyle=':', alpha=0.5, color='#95a5a6')

plt.tight_layout()
plt.savefig(f'{asset_dir}/mapa_micro_guayquichuma.png', dpi=300)
plt.close()
print("Mapa micro perfeccionado.")
