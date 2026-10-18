import urllib.request
import json
import os
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import shape

vault_dir = 'd:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro'
asset_dir = f'{vault_dir}/asset'
raw_data_dir = 'd:/07_Ciclo/septimo_ciclo/public_investment_projects/data/raw'
os.makedirs(asset_dir, exist_ok=True)
os.makedirs(raw_data_dir, exist_ok=True)

headers = {'User-Agent': 'UNL-Economia-Project-Torata/1.0'}

def fetch_geojson(query):
    url = f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&polygon_geojson=1'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode())
        for item in res:
            if 'geojson' in item and item['geojson']['type'] in ['Polygon', 'MultiPolygon']:
                return item
    return None

print("Descargando o cargando polígonos...")
torata_geojson_path = f'{raw_data_dir}/torata_boundary.geojson'
sr_geojson_path = f'{raw_data_dir}/santarosa_boundary.geojson'

if os.path.exists(torata_geojson_path) and os.path.exists(sr_geojson_path):
    with open(torata_geojson_path, 'r', encoding='utf-8') as f:
        geom_torata = shape(json.load(f))
    with open(sr_geojson_path, 'r', encoding='utf-8') as f:
        geom_sr = shape(json.load(f))
else:
    torata_data = fetch_geojson('Torata, Santa Rosa, El Oro, Ecuador')
    santarosa_data = fetch_geojson('Santa Rosa, El Oro, Ecuador')
    geom_torata = shape(torata_data['geojson']) if torata_data else None
    geom_sr = shape(santarosa_data['geojson']) if santarosa_data else None

gdf_sr = gpd.GeoDataFrame([{'name': 'Cantón Santa Rosa', 'geometry': geom_sr}], crs='EPSG:4326') if geom_sr else None
gdf_torata = gpd.GeoDataFrame([{'name': 'Parroquia Torata', 'geometry': geom_torata}], crs='EPSG:4326') if geom_torata else None

# ----------------- MAPA 1: Macro-localización Cantonal -----------------
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

if gdf_sr is not None:
    gdf_sr.plot(ax=ax, color='#e8f8f5', edgecolor='#16a085', linewidth=1.5, label='Cantón Santa Rosa')
if gdf_torata is not None:
    gdf_torata.plot(ax=ax, color='#fdebd0', edgecolor='#d35400', linewidth=2.0, label='Parroquia Torata (8.538,00 ha)')

# Puntos clave cantonales
puntos_macro = [
    ('Torata (Cabecera Parroquial)', -79.8820, -3.5650, '#c0392b'),
    ('Santa Rosa (Cabecera Cantonal)', -79.9667, -3.4500, '#2980b9'),
    ('Bellavista', -79.9050, -3.5120, '#7f8c8d'),
    ('La Avanzada', -79.9350, -3.5200, '#7f8c8d'),
    ('San Antonio', -79.9800, -3.4200, '#7f8c8d')
]

for label, lon, lat, col in puntos_macro:
    ax.plot(lon, lat, marker='o', color=col, markersize=5 if 'Santa Rosa' in label else 4)
    offset_x = 0.015 if 'Santa Rosa' in label else 0.01
    ax.text(lon + offset_x, lat, label, fontsize=6.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85, edgecolor=col, linewidth=0.6))

if geom_sr is not None:
    minx, miny, maxx, maxy = geom_sr.bounds
    pad_x = (maxx - minx) * 0.08
    pad_y = (maxy - miny) * 0.08
    ax.set_xlim(minx - pad_x, maxx + pad_x)
    ax.set_ylim(miny - pad_y, maxy + pad_y)

ax.set_title('Macro-localización: Parroquia Torata en el Cantón Santa Rosa', fontsize=9.5, fontweight='bold', pad=10)
ax.set_xlabel('Longitud (WGS84)', fontsize=7)
ax.set_ylabel('Latitud (WGS84)', fontsize=7)
ax.tick_params(labelsize=6)
ax.grid(True, linestyle=':', alpha=0.5, color='gray')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#e8f8f5', edgecolor='#16a085', label='Cantón Santa Rosa'),
    Patch(facecolor='#fdebd0', edgecolor='#d35400', label='Parroquia Torata')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=6.5, framealpha=0.9)

plt.tight_layout()
plt.savefig(f'{asset_dir}/mapa_macro_torata.png', dpi=300)
plt.close()

# ----------------- MAPA 2: Micro-localización Parroquial -----------------
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

if gdf_torata is not None:
    gdf_torata.plot(ax=ax, color='#fef9e7', edgecolor='#b7950b', linewidth=2.0)

# Asentamientos / sitios de Torata
sitios_torata = [
    ('Torata Centro', -79.8820, -3.5650, '#c0392b'),
    ('El Playón', -79.8650, -3.5800, '#8e44ad'),
    ('La Chilca', -79.8920, -3.5450, '#27ae60'),
    ('Sabayán', -79.8550, -3.5950, '#d35400'),
    ('El Guayabo', -79.8700, -3.6100, '#2980b9'),
    ('La Pereira', -79.8850, -3.6250, '#16a085')
]

for label, lon, lat, col in sitios_torata:
    ax.plot(lon, lat, marker='s', color=col, markersize=4)
    ax.text(lon + 0.003, lat, label, fontsize=6.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor=col, linewidth=0.6))

if geom_torata is not None:
    minx, miny, maxx, maxy = geom_torata.bounds
    pad_x = (maxx - minx) * 0.12
    pad_y = (maxy - miny) * 0.12
    ax.set_xlim(minx - pad_x, maxx + pad_x)
    ax.set_ylim(miny - pad_y, maxy + pad_y)

ax.set_title('Micro-localización: Comunidades y Asentamientos de Torata', fontsize=9.5, fontweight='bold', pad=10)
ax.set_xlabel('Longitud (WGS84)', fontsize=7)
ax.set_ylabel('Latitud (WGS84)', fontsize=7)
ax.tick_params(labelsize=6)
ax.grid(True, linestyle=':', alpha=0.5, color='gray')

from matplotlib.lines import Line2D
legend_micro = [
    Patch(facecolor='#fef9e7', edgecolor='#b7950b', label='Límite Parroquial Torata'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#c0392b', markersize=5, label='Cabecera Parroquial'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#8e44ad', markersize=4, label='Sitios y Comunidades')
]
ax.legend(handles=legend_micro, loc='lower right', fontsize=6.5, framealpha=0.9)

plt.tight_layout()
plt.savefig(f'{asset_dir}/mapa_micro_torata.png', dpi=300)
plt.close()

print("Mapas generados exitosamente en asset/")
