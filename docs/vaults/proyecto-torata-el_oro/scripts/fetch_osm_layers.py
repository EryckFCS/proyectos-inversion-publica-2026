import json
import urllib.request
import os

raw_data_dir = "d:/07_Ciclo/septimo_ciclo/public_investment_projects/data/raw"

# Consultar vías y límites vecinos de Torata en OpenStreetMap
query = """[out:json][timeout:30];
(
  way["highway"](-3.64,-79.94,-3.54,-79.75);
  relation["admin_level"="8"]["name"="La Avanzada"];
  relation["admin_level"="8"]["name"="Bellamaría"];
  relation["admin_level"="8"]["name"="Saracay"];
);
out body;
>;
out skel qt;
"""

url = "https://overpass-api.de/api/interpreter"
req = urllib.request.Request(url, data=query.encode("utf-8"), headers={"User-Agent": "UNL-PIP-Torata/1.0"})

try:
    print("Consultando Overpass API...")
    with urllib.request.urlopen(req, timeout=35) as resp:
        data = json.loads(resp.read().decode())
        with open(f"{raw_data_dir}/overpass_torata_infra.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
    print("Overpass data guardada con éxito:", len(data.get("elements", [])), "elementos.")
except Exception as e:
    print("Error consultando Overpass:", e)

