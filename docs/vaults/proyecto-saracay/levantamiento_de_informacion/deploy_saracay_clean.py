import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# Descargar las 41 preguntas de a2BAHpQdZRvJy7vb8NndDU
res = requests.get(f"{BASE_URL}/api/v2/assets/a2BAHpQdZRvJy7vb8NndDU/", headers=headers)
content = res.json().get("content", {})
survey = content.get("survey", [])
choices = content.get("choices", [])

# En ODK/Kobo: cuando se cierra un grupo, el type es 'end_group' y NO debe llevar 'name' arbitrario, o debe ser 'end_group'
for q in survey:
    if q.get("type") == "end_group":
        # Eliminar name si termina en _end o dejar vacío
        if "name" in q:
            del q["name"]

payload_asset = {
    "name": "Encuesta Diagnóstico Territorial y Saneamiento Básico - Parroquia Saracay (UNL)",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": survey,
        "choices": choices,
        "settings": {
            "title": "Diagnóstico Territorial Saracay - UNL",
            "id_string": "saracay_diagnostico_unl_2026"
        }
    })
}

res_create = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=payload_asset)
print("Create Status:", res_create.status_code)
asset_data = res_create.json()
asset_uid = asset_data.get("uid")
print("Asset UID:", asset_uid)

res_deploy = requests.post(
    f"{BASE_URL}/api/v2/assets/{asset_uid}/deployment/",
    headers=headers_dep,
    data={"active": "true"}
)
print("Deploy Status:", res_deploy.status_code)

if res_deploy.status_code in [200, 201]:
    res_final = requests.get(f"{BASE_URL}/api/v2/assets/{asset_uid}/", headers=headers)
    final_data = res_final.json()
    links = final_data.get("deployment__links", {})
    print("\n" + "="*70)
    print("¡FORMULARIO SARACAY DESPLEGADO EXITOSAMENTE!")
    print(f"UID del Formulario: {asset_uid}")
    print(f"URL Web Enketo (Online): {links.get('url')}")
    print(f"URL Envío Único: {links.get('single_url')}")
    print(f"URL Offline (Kobo App / Enketo Offline): {links.get('offline_url')}")
    print("="*70)
else:
    print("Error:", res_deploy.text[:400])
