import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}

# 1. Crear un formulario mínimo de prueba
payload = {
    "name": "Test Saracay Simple",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": [
            {
                "type": "text",
                "name": "nombre",
                "label": "Nombre del entrevistado"
            }
        ],
        "choices": [],
        "settings": {}
    })
}

res = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=payload)
print("Create minimal asset status:", res.status_code)
data = res.json()
uid = data.get("uid")
print("UID:", uid)

# 2. Desplegar
res_dep = requests.post(
    f"{BASE_URL}/api/v2/assets/{uid}/deployment/",
    headers={"Authorization": f"Token {TOKEN}", "Accept": "application/json"},
    data={"active": "true"}
)
print("Deploy minimal status:", res_dep.status_code)
if res_dep.status_code == 201:
    res_final = requests.get(f"{BASE_URL}/api/v2/assets/{uid}/", headers=headers)
    print("Links:", json.dumps(res_final.json().get("deployment__links", {}), indent=2))
else:
    print("Deploy text:", res_dep.text[:400])
