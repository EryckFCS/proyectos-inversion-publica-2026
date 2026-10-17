import requests
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
asset_uid = "aSW6Fr4FbB37CiqFfPoMZd"

# Check validation status
res = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/validation_status/", headers=headers)
print("Validation status:", res.status_code, res.text)

# Inspect content
res_c = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
data = res_c.json()
print("Settings:", data.get("content", {}).get("settings"))
print("Translations:", data.get("content", {}).get("translations"))
print("Summary:", data.get("summary"))
