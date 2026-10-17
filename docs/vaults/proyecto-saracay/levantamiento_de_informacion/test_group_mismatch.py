import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# En el script anterior usamos:
# {"name": "grp_control", "type": "begin_group", ...}
# {"name": "grp_control_end", "type": "end_group"}  <-- NOTA: name diferente!
# En ODK y Kobo, end_group DEBE tener el mismo name que begin_group o no llevar name!

asset_payload = {
    "name": "Test Group Mismatch",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": [
            {"type": "begin_group", "name": "grp1", "label": "Grupo 1"},
            {"type": "text", "name": "pregunta1", "label": "Pregunta"},
            {"type": "end_group", "name": "grp1_end"}
        ],
        "choices": [],
        "settings": {}
    })
}
res = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=asset_payload)
uid = res.json().get("uid")
res_dep = requests.post(f"{BASE_URL}/api/v2/assets/{uid}/deployment/", headers=headers_dep, data={"active": "true"})
print("Mismatch end_group name:", res_dep.status_code)
