import requests
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
asset_uid = "aDrLC6UgnmU2q4VS8b8M4t"

# Endpoint de creación de nuevo asset tipo survey o clone
res = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
data = res.json()
print("Asset keys:", data.keys())
print("Has deployment:", data.get("has_deployment"))
print("Deployed version id:", data.get("deployed_version_id"))
print("Version id:", data.get("version_id"))
print("Submissions url:", data.get("data"))
