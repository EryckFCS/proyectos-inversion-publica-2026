import os
import json
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon as MplPolygon, FancyBboxPatch
from shapely.geometry import shape, Polygon, MultiPolygon
import geopandas as gpd

print("Iniciando generación de mapa técnico estilo PDOT Torata...")
output_path = "d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro/asset/mapa_tecnico_torata.png"
raw_data_dir = "d:/07_Ciclo/septimo_ciclo/public_investment_projects/data/raw"

# Cargar límites
with open(f"{raw_data_dir}/torata_boundary.geojson", "r", encoding="utf-8") as f:
    torata_geom = shape(json.load(f))

with open(f"{raw_data_dir}/santarosa_boundary.geojson", "r", encoding="utf-8") as f:
    sr_geom = shape(json.load(f))

print("Geometrías base cargadas.")

