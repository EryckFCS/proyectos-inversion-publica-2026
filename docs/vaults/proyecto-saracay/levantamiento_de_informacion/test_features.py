import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# 1. Probar geopoint + image + note
asset_payload = {
    "name": "Test Geopoint Image",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": [
            {"type": "start", "name": "start"},
            {"type": "end", "name": "end"},
            {"type": "today", "name": "today"},
            {"type": "geopoint", "name": "gps", "label": "GPS"},
            {"type": "image", "name": "foto", "label": "Foto"},
            {"type": "note", "name": "nota", "label": "Nota final"}
        ],
        "choices": [],
        "settings": {}
    })
}
res = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=asset_payload)
uid = res.json().get("uid")
res_dep = requests.post(f"{BASE_URL}/api/v2/assets/{uid}/deployment/", headers=headers_dep, data={"active": "true"})
print("Test geopoint + image:", res_dep.status_code)

# 2. Probar relevant expression
asset_payload2 = {
    "name": "Test Relevant",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": [
            {"type": "select_one", "select_from_list_name": "list_sino", "name": "tiene_otro", "label": "¿Tiene otro?"},
            {"type": "text", "name": "cual_otro", "label": "¿Cuál otro?", "relevant": "${tiene_otro} = 'otro'"}
        ],
        "choices": [
            {"list_name": "list_sino", "name": "si", "label": "Sí"},
            {"list_name": "list_sino", "name": "otro", "label": "Otro"}
        ],
        "settings": {}
    })
}
res2 = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=asset_payload2)
uid2 = res2.json().get("uid")
res_dep2 = requests.post(f"{BASE_URL}/api/v2/assets/{uid2}/deployment/", headers=headers_dep, data={"active": "true"})
print("Test relevant syntax:", res_dep2.status_code)
