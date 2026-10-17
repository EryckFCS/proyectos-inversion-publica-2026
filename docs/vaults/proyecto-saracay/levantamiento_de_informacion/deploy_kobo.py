import requests
import json
import time

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}"}
import_uid = "iX4wzSJ6rNebYvYArQaqq3"

print("Consultando estado de importación...")
for _ in range(10):
    res = requests.get(f"https://kf.kobotoolbox.org/api/v2/imports/{import_uid}/", headers=headers)
    data = res.json()
    status = data.get("status")
    print("Status:", status)
    if status == "complete":
        messages = data.get("messages", {})
        asset_uid = messages.get("created", [None])[0]
        print("Created Asset UID:", asset_uid)
        
        # Desplegar asset
        if asset_uid:
            print("Desplegando formulario...")
            res_dep = requests.post(
                f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/deployment/",
                headers=headers,
                data={"active": True}
            )
            print("Deploy response:", res_dep.status_code, res_dep.text)
            
            # Consultar asset info
            res_asset = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
            asset_info = res_asset.json()
            deployment = asset_info.get("deployment__links", {})
            print("\nURLs de despliegue:")
            print(json.dumps(deployment, indent=2))
        break
    elif status == "error":
        print("Error en importación:", data.get("messages"))
        break
    time.sleep(2)
