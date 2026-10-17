import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
ASSET_UID = "aDrLC6UgnmU2q4VS8b8M4t"
BASE_URL = "https://kf.kobotoolbox.org"

url = f"{BASE_URL}/api/v2/assets/{ASSET_UID}/deployment/"
headers = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json"
}
payload = {
    "active": "true"
}

response = requests.post(url, headers=headers, data=payload)
print("Response code:", response.status_code)
try:
    print(response.json())
except:
    print(response.text[:300])

if response.status_code == 201:
    res_asset = requests.get(f"{BASE_URL}/api/v2/assets/{ASSET_UID}/", headers=headers)
    links = res_asset.json().get("deployment__links", {})
    print("\n¡DESPLIEGUE EXITOSO!")
    print(json.dumps(links, indent=2))
