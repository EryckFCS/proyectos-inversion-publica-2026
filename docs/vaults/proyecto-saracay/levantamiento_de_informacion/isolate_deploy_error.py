import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# 1. Probar con solo 1 pregunta select_one y choices
asset_payload = {
    "name": "Test Select One",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": [
            {"type": "select_one", "select_from_list_name": "list_sino", "name": "preg1", "label": "¿Tiene agua potable?"}
        ],
        "choices": [
            {"list_name": "list_sino", "name": "si", "label": "Sí"},
            {"list_name": "list_sino", "name": "no", "label": "No"}
        ],
        "settings": {}
    })
}
res = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=asset_payload)
uid = res.json().get("uid")
res_dep = requests.post(f"{BASE_URL}/api/v2/assets/{uid}/deployment/", headers=headers_dep, data={"active": "true"})
print("Test 1 (select_one):", res_dep.status_code)

# 2. Probar con begin_group
asset_payload2 = {
    "name": "Test Group",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": [
            {"type": "begin_group", "name": "grp1", "label": "Grupo 1"},
            {"type": "text", "name": "nombre", "label": "Nombre"},
            {"type": "end_group", "name": "grp1"}
        ],
        "choices": [],
        "settings": {}
    })
}
res2 = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=asset_payload2)
uid2 = res2.json().get("uid")
res_dep2 = requests.post(f"{BASE_URL}/api/v2/assets/{uid2}/deployment/", headers=headers_dep, data={"active": "true"})
print("Test 2 (begin_group con name igual):", res_dep2.status_code)

# 3. Probar select_multiple
asset_payload3 = {
    "name": "Test Select Multiple",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": [
            {"type": "select_multiple", "select_from_list_name": "list_act", "name": "actividades", "label": "Actividades"}
        ],
        "choices": [
            {"list_name": "list_act", "name": "agri", "label": "Agricultura"},
            {"list_name": "list_act", "name": "comer", "label": "Comercio"}
        ],
        "settings": {}
    })
}
res3 = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=asset_payload3)
uid3 = res3.json().get("uid")
res_dep3 = requests.post(f"{BASE_URL}/api/v2/assets/{uid3}/deployment/", headers=headers_dep, data={"active": "true"})
print("Test 3 (select_multiple):", res_dep3.status_code)
