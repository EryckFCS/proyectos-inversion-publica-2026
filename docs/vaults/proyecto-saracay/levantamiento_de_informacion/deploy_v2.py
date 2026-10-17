import requests
import json
import time

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
import_uid = "irC9Vk7zFNMaSTbqAHegY9"

print("Consultando importación...")
for _ in range(10):
    res = requests.get(f"https://kf.kobotoolbox.org/api/v2/imports/{import_uid}/", headers=headers)
    data = res.json()
    status = data.get("status")
    print("Status:", status)
    if status == "complete":
        created = data.get("messages", {}).get("created", [None])[0]
        asset_uid = created.get("uid") if isinstance(created, dict) else created
        print("Created Asset UID:", asset_uid)
        
        # Deploy asset
        res_dep = requests.post(
            f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/deployment/",
            headers=headers
        )
        print("Deploy status:", res_dep.status_code)
        if res_dep.status_code != 201:
            print("Deploy text:", res_dep.text[:400])
            
        res_asset = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
        asset_info = res_asset.json()
        print("\nDEPLOYMENT LINKS:")
        print(json.dumps(asset_info.get("deployment__links", {}), indent=2))
        break
    time.sleep(2)
