import requests
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
asset_uid = "aSW6Fr4FbB37CiqFfPoMZd"

# Obtener asset info
res = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
asset_data = res.json()
version_id = asset_data.get("version_id")
print(f"Asset Name: {asset_data.get('name')}")
print(f"Version ID: {version_id}")
print(f"Status: {asset_data.get('status')}")

# Desplegar por primera vez vía POST a /api/v2/assets/{asset_uid}/deployment/
# Nota: Kobo v2 para crear el primer deployment requiere POST
res_deploy = requests.post(
    f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/deployment/",
    headers=headers,
    json={"version_id": version_id}
)
print("Deploy POST:", res_deploy.status_code, res_deploy.text)

if res_deploy.status_code != 201:
    # Intento con PATCH
    res_patch = requests.patch(
        f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/deployment/",
        headers=headers,
        json={"active": True, "version_id": version_id}
    )
    print("Deploy PATCH:", res_patch.status_code, res_patch.text)

# Consultar links
res_final = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
data_final = res_final.json()
print("\n--- ENLACES OFICIALES ---")
print("Enketo web link:", data_final.get("deployment__links", {}).get("url"))
print("Single submission link:", data_final.get("deployment__links", {}).get("single_url"))
print("Offline link:", data_final.get("deployment__links", {}).get("offline_url"))
