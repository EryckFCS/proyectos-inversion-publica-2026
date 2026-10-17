import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

res = requests.get(f"{BASE_URL}/api/v2/assets/a2BAHpQdZRvJy7vb8NndDU/", headers=headers)
content = res.json().get("content", {})
survey = content.get("survey", [])
choices = content.get("choices", [])

# Sin grupos
flat_survey = [q for q in survey if q.get("type") not in ["begin_group", "end_group"]]
list_names = {q.get("select_from_list_name") for q in flat_survey if q.get("select_from_list_name")}
flat_choices = [c for c in choices if c.get("list_name") in list_names]

payload = {
    "name": "Encuesta Diagnostico Territorial Saracay (UNL)",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": flat_survey,
        "choices": flat_choices,
        "settings": {
            "title": "Diagnostico Territorial Saracay - UNL",
            "id_string": "saracay_diagnostico_2026"
        }
    })
}

res_create = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=payload)
print("Create status:", res_create.status_code)
uid = res_create.json().get("uid")
print("Asset UID:", uid)

res_dep = requests.post(
    f"{BASE_URL}/api/v2/assets/{uid}/deployment/",
    headers=headers_dep,
    data={"active": "true"}
)
print("Deploy status:", res_dep.status_code)

if res_dep.status_code in [200, 201]:
    res_final = requests.get(f"{BASE_URL}/api/v2/assets/{uid}/", headers=headers)
    links = res_final.json().get("deployment__links", {})
    print("\n" + "="*70)
    print("¡DESPLIEGUE EXITOSO!")
    print(f"UID: {uid}")
    print(f"Enkento Web: {links.get('url')}")
    print(f"Single URL: {links.get('single_url')}")
    print(f"Offline URL: {links.get('offline_url')}")
    print("="*70)
else:
    print("Deploy text:", res_dep.text[:400])
