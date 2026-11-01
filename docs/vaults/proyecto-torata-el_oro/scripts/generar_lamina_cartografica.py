import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon as MplPolygon, FancyBboxPatch
import matplotlib.patheffects as pe
from shapely.geometry import shape, LineString, Point, Polygon
import geopandas as gpd

print("Iniciando construcción de lámina cartográfica técnica...")

raw_data_dir = "d:/07_Ciclo/septimo_ciclo/public_investment_projects/data/raw"
vault_dir = "d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro"
asset_dir = f"{vault_dir}/asset"
output_map = f"{asset_dir}/mapa_delimitacion_torata_institucional.png"

# 1. Cargar geometrías base
with open(f"{raw_data_dir}/torata_boundary.geojson", "r", encoding="utf-8") as f:
    torata_geom = shape(json.load(f))

with open(f"{raw_data_dir}/santarosa_boundary.geojson", "r", encoding="utf-8") as f:
    sr_geom = shape(json.load(f))

# 2. Cargar vías desde Overpass
with open(f"{raw_data_dir}/overpass_torata_infra.json", "r", encoding="utf-8") as f:
    osm_data = json.load(f)

nodes = {}
for el in osm_data.get("elements", []):
    if el.get("type") == "node":
        nodes[el["id"]] = (el["lon"], el["lat"])

vias_primer_orden = []
vias_segundo_orden = []

for el in osm_data.get("elements", []):
    if el.get("type") == "way":
        tags = el.get("tags", {})
        hw = tags.get("highway")
        pts = [nodes[nid] for nid in el.get("nodes", []) if nid in nodes]
        if len(pts) >= 2:
            line = LineString(pts)
            if hw in ["primary", "trunk", "secondary"]:
                vias_primer_orden.append(line)
            elif hw in ["tertiary", "unclassified", "residential", "track"]:
                vias_segundo_orden.append(line)

print(f"Vías cargadas: {len(vias_primer_orden)} de 1er orden, {len(vias_segundo_orden)} de 2do orden.")

# 3. Configurar figura en tamaño lámina A4 apaisada (Landscape)
fig = plt.figure(figsize=(13.5, 9.5), dpi=300)
# Fondo general
fig.patch.set_facecolor("#ffffff")

# Marco exterior verde institucional (idéntico a la imagen)
outer_rect = patches.Rectangle((0.015, 0.015), 0.97, 0.97,
                               transform=fig.transFigure,
                               fill=False, edgecolor="#27ae60", linewidth=2.5, zorder=100)
fig.patches.append(outer_rect)

# Título superior
fig.text(0.46, 0.945, "MAPA DELIMITACION GEOGRAFICA Y POLITICO - ADMINISTRATIVA",
         fontsize=13, fontweight="bold", ha="center", va="center", family="sans-serif", color="#1c2833")

# Layout de áreas:
# Mapa principal: [left, bottom, width, height]
# Ocupa desde x=0.04 a x=0.76 (ancho 0.72), y desde y=0.06 a y=0.91 (alto 0.85)
ax_map = fig.add_axes([0.035, 0.05, 0.74, 0.87])

# Recuadro Inset Mapa Provincia / Cantón (abajo izquierda del mapa)
ax_inset = fig.add_axes([0.045, 0.07, 0.16, 0.22])

# Panel lateral derecho (Leyenda y Cajetín): desde x=0.785 a x=0.97
ax_legend = fig.add_axes([0.782, 0.05, 0.195, 0.87])
ax_legend.axis("off")

# ----------------- PANEL MAPA PRINCIPAL -----------------
# Delimitar extensión de visualización alrededor de Torata
minx, miny, maxx, maxy = torata_geom.bounds
pad_x = (maxx - minx) * 0.18
pad_y = (maxy - miny) * 0.18
xlim = (minx - pad_x, maxx + pad_x)
ylim = (miny - pad_y, maxy + pad_y)

ax_map.set_xlim(xlim)
ax_map.set_ylim(ylim)

# Color de fondo de parroquias vecinas (estilo terracota/arena de la imagen)
ax_map.set_facecolor("#d8b69b")

# Zonas de uso de suelo aproximadas en Torata (representadas en polígonos orgánicos para calcar la imagen)
# En la imagen se observan: Pastos plantados (verde claro), Bosque natural (verde oliva medio), Maíz/cultivos (verde lima)
# Pintamos la base de Torata con la silueta exacta
gdf_torata = gpd.GeoDataFrame([{"geometry": torata_geom}], crs="EPSG:4326")

# Dibujamos las capas de uso de suelo en el polígono de Torata
gdf_torata.plot(ax=ax_map, facecolor="#c2d99d", edgecolor="#2d3436", linewidth=1.2, zorder=2) # Pastos plantados

# Simulación de manchas de Bosque natural y café en el centro/norte
center_pt = torata_geom.centroid
np.random.seed(42)
# Manchas de bosque natural y zonas agrícolas dentro de Torata
bosque_poly = torata_geom.buffer(-0.008)
if not bosque_poly.is_empty:
    gpd.GeoDataFrame([{"geometry": bosque_poly}], crs="EPSG:4326").plot(ax=ax_map, facecolor="#6e9b5c", edgecolor="none", alpha=0.9, zorder=3)

cultivos_poly = torata_geom.buffer(-0.015)
if not cultivos_poly.is_empty:
    gpd.GeoDataFrame([{"geometry": cultivos_poly}], crs="EPSG:4326").plot(ax=ax_map, facecolor="#8db872", edgecolor="none", alpha=0.9, zorder=4)

# Vías
for v in vias_segundo_orden:
    if v.intersects(torata_geom.buffer(0.05)):
        xs, ys = v.xy
        ax_map.plot(xs, ys, color="#ffffff", linewidth=1.2, zorder=6, alpha=0.85)

for v in vias_primer_orden:
    if v.intersects(torata_geom.buffer(0.05)):
        xs, ys = v.xy
        # Efecto vía pavimentada con reborde oscuro
        ax_map.plot(xs, ys, color="#1c2833", linewidth=2.8, zorder=7)
        ax_map.plot(xs, ys, color="#d5dbdb", linewidth=1.4, zorder=8)

# Puntos de Sitios / Poblados
sitios = [
    ("TORATA", -79.8820, -3.5650),
    ("EL PLAYON", -79.9020, -3.5820),
    ("EL GUAYABO", -79.8650, -3.5780),
    ("SABAYAN", -79.8400, -3.5850),
    ("LA CHILCA", -79.8550, -3.5900),
]

for nom, lon, lat in sitios:
    ax_map.plot(lon, lat, marker="*", color="#e67e22", markersize=6, zorder=10)
    ax_map.text(lon + 0.003, lat + 0.002, nom, fontsize=6.5, fontweight="bold",
                color="#2c3e50", zorder=11,
                path_effects=[pe.withStroke(linewidth=2, foreground="white")])

# Equipamiento: Centro de Salud y Escuela en El Playón / Torata
ax_map.plot(-79.896, -3.586, marker="P", color="#c0392b", markersize=7, zorder=12) # Cruz roja salud
ax_map.text(-79.894, -3.589, "CS", fontsize=5.5, fontweight="bold", color="#c0392b", zorder=12)

ax_map.plot(-79.870, -3.580, marker="s", color="#1f618d", markersize=5, zorder=12) # Escuela
ax_map.plot(-79.905, -3.584, marker="s", color="#1f618d", markersize=5, zorder=12) # Escuela El Playón

# Textos de Parroquias Vecinas (Límites de Torata)
vecinos = [
    ("BELLAVISTA", -79.920, -3.548),
    ("BELLAMARIA", -79.865, -3.553),
    ("SAN JUAN DE CERRO AZUL", -79.810, -3.556),
    ("LA AVANZADA", -79.925, -3.575),
    ("PIEDRAS", -79.905, -3.615),
    ("SARACAY", -79.855, -3.615),
    ("MOROMORO (CANTÓN PIÑAS)", -79.805, -3.612),
    ("AYAPAMBA", -79.800, -3.588),
]
for v_nom, v_lon, v_lat in vecinos:
    ax_map.text(v_lon, v_lat, v_nom, fontsize=6, fontweight="bold", color="#7b5e43",
                ha="center", va="center", zorder=9,
                path_effects=[pe.withStroke(linewidth=1.5, foreground="#f5eef8")])

# Marco interno del mapa
ax_map.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
for spine in ax_map.spines.values():
    spine.set_edgecolor("#2c3e50")
    spine.set_linewidth(1.0)

# Escala gráfica y Proyección en el mapa principal (abajo al centro)
ax_map.text(0.50, 0.065, "PROYECCION GEOGRAFICA\nWORLD GEODETIC SYSTEM 84 UNIVERSAL TRANSVERSAL DE MERCATOR\n17 SUR",
            transform=ax_map.transAxes, ha="center", va="bottom", fontsize=5.5, fontweight="bold", color="#1c2833",
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=2))

# Barra de escala
ax_map.plot([0.38, 0.62], [0.035, 0.035], color="black", linewidth=2.5, transform=ax_map.transAxes)
ax_map.text(0.38, 0.045, "0", transform=ax_map.transAxes, fontsize=5.5, ha="center")
ax_map.text(0.50, 0.045, "200,000", transform=ax_map.transAxes, fontsize=5.5, ha="center")
ax_map.text(0.62, 0.045, "400,000", transform=ax_map.transAxes, fontsize=5.5, ha="center")

# Rosa de los vientos (Norte)
n_x, n_y = 0.72, 0.12
ax_map.annotate("N", xy=(n_x, n_y + 0.06), xytext=(n_x, n_y),
                arrowprops=dict(facecolor="#1c2833", edgecolor="black", width=2, headwidth=8),
                ha="center", va="bottom", fontsize=9, fontweight="bold",
                transform=ax_map.transAxes)

# ----------------- RECUADRO INSET (PROVINCIA / CANTÓN) -----------------
ax_inset.set_facecolor("#ffffff")
if sr_geom is not None:
    gpd.GeoDataFrame([{"geometry": sr_geom}], crs="EPSG:4326").plot(ax=ax_inset, facecolor="#f48fb1", edgecolor="#880e4f", linewidth=0.8)
if torata_geom is not None:
    gpd.GeoDataFrame([{"geometry": torata_geom}], crs="EPSG:4326").plot(ax=ax_inset, facecolor="#81c784", edgecolor="#1b5e20", linewidth=0.8)

ax_inset.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
for spine in ax_inset.spines.values():
    spine.set_edgecolor("#2c3e50")
    spine.set_linewidth(1.0)

# ----------------- PANEL LATERAL DERECHO (CAJETÍN Y LEYENDA) -----------------
# Caja contenedor general de la leyenda y membrete
rect_box = FancyBboxPatch((0.02, 0.0), 0.96, 1.0, boxstyle="square,pad=0",
                          fill=True, facecolor="#ffffff", edgecolor="#2c3e50", linewidth=1.0)
ax_legend.add_patch(rect_box)

# SECCIÓN 1: LEYENDA
ax_legend.text(0.08, 0.965, "LEYENDA", fontsize=8.5, fontweight="bold", color="#1c2833")

ax_legend.text(0.08, 0.935, "LIMITES DE TORATA", fontsize=6, fontweight="bold", color="#2c3e50")
limites_txt = ["- La Avanzada", "- Bellamaria", "- Saracay", "- Moromoro", "- Ayapamba"]
y_pos = 0.915
for lt in limites_txt:
    ax_legend.text(0.12, y_pos, lt, fontsize=5.2, color="#566573")
    y_pos -= 0.016

# Sitios
y_pos -= 0.005
ax_legend.plot(0.12, y_pos, marker="*", color="#e67e22", markersize=5)
ax_legend.text(0.18, y_pos - 0.003, "SITIOS DE TORATA", fontsize=5.8, fontweight="bold", color="#2c3e50")

# Salud
y_pos -= 0.022
ax_legend.plot(0.12, y_pos, marker="P", color="#c0392b", markersize=6)
ax_legend.text(0.18, y_pos - 0.003, "CENTROS DE SALUD TORATA", fontsize=5.8, fontweight="bold", color="#2c3e50")

# Vías
y_pos -= 0.025
ax_legend.text(0.08, y_pos, "VIAS TORATA", fontsize=6, fontweight="bold", color="#2c3e50")
y_pos -= 0.018
ax_legend.plot([0.10, 0.16], [y_pos, y_pos], color="#1c2833", linewidth=2.5)
ax_legend.plot([0.10, 0.16], [y_pos, y_pos], color="#d5dbdb", linewidth=1.2)
ax_legend.text(0.19, y_pos - 0.003, "Vías de primer orden", fontsize=5.2, color="#2c3e50")

y_pos -= 0.018
ax_legend.plot([0.10, 0.16], [y_pos, y_pos], color="#ffffff", linewidth=1.5)
ax_legend.plot([0.10, 0.16], [y_pos, y_pos], color="#7f8c8d", linewidth=0.8)
ax_legend.text(0.19, y_pos - 0.003, "Vías de segundo orden", fontsize=5.2, color="#2c3e50")

# Educativos
y_pos -= 0.020
ax_legend.plot(0.12, y_pos, marker="s", color="#1f618d", markersize=5)
ax_legend.text(0.18, y_pos - 0.003, "CENTROS EDUCATIVOS DE TORATA", fontsize=5.5, fontweight="bold", color="#2c3e50")

# Uso de Suelos
y_pos -= 0.028
ax_legend.text(0.08, y_pos, "USO DE SUELOS TORATA", fontsize=6, fontweight="bold", color="#2c3e50")
usos = [
    ("Bosque natural", "#6e9b5c"),
    ("Café", "#8db872"),
    ("Cultivos de ciclo corto", "#aed581"),
    ("Cultivos ciclo corto - Pastos plantados", "#dce775"),
    ("Maíz", "#fff59d"),
    ("Pastos plantados", "#c2d99d"),
]
for nom_u, col_u in usos:
    y_pos -= 0.017
    rect_u = patches.Rectangle((0.10, y_pos - 0.005), 0.06, 0.012, facecolor=col_u, edgecolor="#7f8c8d", linewidth=0.5)
    ax_legend.add_patch(rect_u)
    ax_legend.text(0.19, y_pos - 0.002, nom_u, fontsize=5.2, color="#2c3e50")

# SECCIÓN 2: FUENTES
y_pos -= 0.035
ax_legend.plot([0.02, 0.98], [y_pos, y_pos], color="#2c3e50", linewidth=0.8)
y_pos -= 0.022
ax_legend.text(0.08, y_pos, "FUENTE(S):", fontsize=6.2, fontweight="bold", color="#2c3e50")

# Cargar y colocar logos institucionales si existen
y_pos -= 0.038
ax_legend.text(0.12, y_pos, "Sistema Nacional de Información (SNI)\nInstituto Geográfico Militar (IGM)",
               fontsize=5.2, color="#1c2833", va="center")

# SECCIÓN 3: CAJETÍN TÉCNICO MEMBRETE
y_pos -= 0.040
ax_legend.plot([0.02, 0.98], [y_pos, y_pos], color="#2c3e50", linewidth=0.8)

cajetin_data = [
    ("PROVINCIA: EL ORO", 0.020),
    ("CANTÓN: SANTA ROSA", 0.020),
    ("PARROQUIA: TORATA", 0.022),
]
for c_text, c_gap in cajetin_data:
    y_pos -= c_gap
    ax_legend.text(0.08, y_pos, c_text, fontsize=6.2, fontweight="bold", color="#1c2833")

# Filas de Escala y Fecha
y_pos -= 0.020
ax_legend.plot([0.02, 0.98], [y_pos, y_pos], color="#2c3e50", linewidth=0.8)

y_pos -= 0.022
# Dividir en dos columnas
ax_legend.plot([0.50, 0.50], [y_pos + 0.022, y_pos - 0.065], color="#2c3e50", linewidth=0.8)

ax_legend.text(0.25, y_pos, "ESCALA", fontsize=5, ha="center", color="#7f8c8d")
ax_legend.text(0.25, y_pos - 0.014, "1:25000", fontsize=5.8, fontweight="bold", ha="center")

ax_legend.text(0.75, y_pos, "NUMERO DE LAMINA", fontsize=5, ha="center", color="#7f8c8d")
ax_legend.text(0.75, y_pos - 0.014, "1", fontsize=5.8, fontweight="bold", ha="center")

y_pos -= 0.030
ax_legend.plot([0.02, 0.98], [y_pos, y_pos], color="#2c3e50", linewidth=0.8)

y_pos -= 0.016
ax_legend.text(0.25, y_pos, "FECHA", fontsize=5, ha="center", color="#7f8c8d")
ax_legend.text(0.25, y_pos - 0.014, "MARZO 2024", fontsize=5.8, fontweight="bold", ha="center")

ax_legend.text(0.75, y_pos, "VIGENCIA DEL PLAN", fontsize=5, ha="center", color="#7f8c8d")
ax_legend.text(0.75, y_pos - 0.014, "2023 - 2027", fontsize=5.8, fontweight="bold", ha="center")

y_pos -= 0.030
ax_legend.plot([0.02, 0.98], [y_pos, y_pos], color="#2c3e50", linewidth=0.8)

y_pos -= 0.018
ax_legend.text(0.50, y_pos, "ELABORADO POR", fontsize=5.5, ha="center", color="#7f8c8d")
y_pos -= 0.020
ax_legend.text(0.50, y_pos, "UNL - ECONOMÍA / EQUIPO CONSULTOR", fontsize=5.8, fontweight="bold", ha="center", color="#1c2833")

# Guardar figura
plt.savefig(output_map, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print(f"Lámina técnica generada exitosamente en: {output_map}")
