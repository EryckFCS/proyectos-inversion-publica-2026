import requests
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
asset_uid = "aSW6Fr4FbB37CiqFfPoMZd"

# Obtener content actual
res_c = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
data = res_c.json()
content = data.get("content", {})

print("Current translations:", content.get("translations"))
print("Current translated fields:", content.get("translated"))

# Normalizar translations: solo ['Español (es)']
survey = content.get("survey", [])
for q in survey:
    # Si label o hint tienen subdict
    if isinstance(q.get("label"), list):
        q["label"] = q["label"][0] if q["label"] else ""
    if isinstance(q.get("hint"), list):
        q["hint"] = q["hint"][0] if q["hint"] else ""

choices = content.get("choices", [])
for c in choices:
    if isinstance(c.get("label"), list):
        c["label"] = c["label"][0] if c["label"] else ""

new_content = {
    "survey": survey,
    "choices": choices,
    "settings": content.get("settings", {}),
    "translated": ["label", "hint"],
    "translations": ["Spanish (es)"]
}

res_patch = requests.patch(
    f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/",
    headers=headers,
    json={"content": new_content}
)
print("Patch status:", res_patch.status_code)
new_ver = res_patch.json().get("version_id")
print("New version:", new_ver)

# Probar deploy
res_dep = requests.post(
    f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/deployment/",
    headers=headers,
    json={"version_id": new_ver}
)
print("Deploy POST status:", res_dep.status_code)
if res_dep.status_code == 201:
    print("¡Despliegue exitoso!")
    res_final = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
    links = res_final.json().get("deployment__links", {})
    print(json.dumps(links, indent=2))
else:
    print("Error en deploy:", res_dep.text[:500])
