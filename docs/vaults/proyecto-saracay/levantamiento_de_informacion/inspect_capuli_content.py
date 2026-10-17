import requests
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}"}
asset_uid = "aBJEiLwrvSWwb7fBrukk8a"

res = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
data = res.json()
print("Capuli content keys:", data.get("content", {}).keys())
print("Capuli content translated:", data.get("content", {}).get("translated"))
print("Capuli content translations:", data.get("content", {}).get("translations"))
print("Capuli content settings:", data.get("content", {}).get("settings"))
if data.get("content", {}).get("survey"):
    print("Example question:", data.get("content", {}).get("survey")[0])
