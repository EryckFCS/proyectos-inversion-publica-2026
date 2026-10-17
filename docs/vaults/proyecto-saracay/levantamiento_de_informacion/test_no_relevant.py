import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# 1. Probar ${sector_saracay} = 'otro'
survey_rel1 = [
    {"type": "select_one", "select_from_list_name": "list_sino", "name": "sector_saracay", "label": "Sector"},
    {"type": "text", "name": "sector_otro", "label": "Otro sector", "relevant": "${sector_saracay} = 'otro'"}
]
choices = [
    {"list_name": "list_sino", "name": "si", "label": "Sí"},
    {"list_name": "list_sino", "name": "otro", "label": "Otro"}
]

p1 = {"name": "Test Rel 1", "asset_type": "survey", "content": json.dumps({"schema": "1", "survey": survey_rel1, "choices": choices, "settings": {}})}
r1 = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=p1)
uid1 = r1.json().get("uid")
rd1 = requests.post(f"{BASE_URL}/api/v2/assets/{uid1}/deployment/", headers=headers_dep, data={"active": "true"})
print("Test Relevant 1:", rd1.status_code)

# 2. Probar survey de Saracay SIN los campos 'relevant'
res = requests.get(f"{BASE_URL}/api/v2/assets/a2BAHpQdZRvJy7vb8NndDU/", headers=headers)
content = res.json().get("content", {})
survey = content.get("survey", [])
choices_all = content.get("choices", [])

for q in survey:
    if "relevant" in q:
        del q["relevant"]

p2 = {"name": "Test Saracay No Relevant", "asset_type": "survey", "content": json.dumps({"schema": "1", "survey": survey, "choices": choices_all, "settings": {}})}
r2 = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=p2)
uid2 = r2.json().get("uid")
rd2 = requests.post(f"{BASE_URL}/api/v2/assets/{uid2}/deployment/", headers=headers_dep, data={"active": "true"})
print("Test Saracay SIN relevant:", rd2.status_code)
