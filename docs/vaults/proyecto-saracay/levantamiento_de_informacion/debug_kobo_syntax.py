import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
ASSET_UID = "aDrLC6UgnmU2q4VS8b8M4t"
BASE_URL = "https://kf.kobotoolbox.org"

headers = {"Authorization": f"Token {TOKEN}"}

# Ver validación
res = requests.get(f"{BASE_URL}/api/v2/assets/{ASSET_UID}/validation_status/", headers=headers)
print("Validation status:", res.status_code, res.text)

# Ver asset JSON
res = requests.get(f"{BASE_URL}/api/v2/assets/{ASSET_UID}/", headers=headers)
content = res.json().get("content", {})
print("Survey count:", len(content.get("survey", [])))
print("Choices count:", len(content.get("choices", [])))
for q in content.get("survey", [])[:5]:
    print(q)
