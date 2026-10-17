import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
ASSET_UID = "aDrLC6UgnmU2q4VS8b8M4t"
BASE_URL = "https://kf.kobotoolbox.org"

headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}

res = requests.get(f"{BASE_URL}/api/v2/assets/{ASSET_UID}/", headers=headers)
data = res.json()
content = data.get("content", {})
survey = content.get("survey", [])
choices = content.get("choices", [])

def fix_field(val):
    if isinstance(val, list):
        for item in val:
            if item is not None and str(item).strip():
                return str(item).strip()
        return ""
    return str(val) if val is not None else ""

for q in survey:
    if "label" in q:
        q["label"] = fix_field(q["label"])
    if "hint" in q:
        q["hint"] = fix_field(q["hint"])

for c in choices:
    if "label" in c:
        c["label"] = fix_field(c["label"])

new_content = {
    "survey": survey,
    "choices": choices,
    "settings": {},
    "translated": ["label", "hint"],
    "translations": [None]
}

print("Actualizando content limpio...")
res_patch = requests.patch(
    f"{BASE_URL}/api/v2/assets/{ASSET_UID}/",
    headers=headers,
    json={"content": new_content}
)
print("Patch status:", res_patch.status_code)
ver = res_patch.json().get("version_id")
print("New version:", ver)

# Intentar deploy
headers_form = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}
res_dep = requests.post(
    f"{BASE_URL}/api/v2/assets/{ASSET_UID}/deployment/",
    headers=headers_form,
    data={"active": "true", "version_id": ver}
)
print("Deploy POST status:", res_dep.status_code)
if res_dep.status_code == 201:
    print("¡DESPLIEGUE EXITOSO!")
    res_final = requests.get(f"{BASE_URL}/api/v2/assets/{ASSET_UID}/", headers=headers)
    print(json.dumps(res_final.json().get("deployment__links", {}), indent=2))
else:
    print("Deploy text:", res_dep.text[:400])
