import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# Testear cada tipo de pregunta individualmente
preguntas_test = [
    {"type": "text", "name": "p_text", "label": "Texto"},
    {"type": "date", "name": "p_date", "label": "Fecha"},
    {"type": "geopoint", "name": "p_geo", "label": "GPS"},
    {"type": "integer", "name": "p_int", "label": "Entero"},
    {"type": "image", "name": "p_img", "label": "Foto"},
    {"type": "note", "name": "p_note", "label": "Nota"}
]

p = {
    "name": "Test Core Types",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": preguntas_test,
        "choices": [],
        "settings": {}
    })
}
r = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=p)
uid = r.json().get("uid")
rd = requests.post(f"{BASE_URL}/api/v2/assets/{uid}/deployment/", headers=headers_dep, data={"active": "true"})
print("Core types deploy status:", rd.status_code)
