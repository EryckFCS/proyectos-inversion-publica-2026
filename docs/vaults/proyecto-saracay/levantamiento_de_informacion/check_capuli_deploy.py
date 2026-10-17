import requests
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
asset_uid = "aBJEiLwrvSWwb7fBrukk8a"

res = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
data = res.json()
print("Capuli deployment info:")
print("Status:", data.get("status"))
print("Deployment links:", json.dumps(data.get("deployment__links", {}), indent=2))
print("Deployed version:", data.get("deployed_version_id"))
