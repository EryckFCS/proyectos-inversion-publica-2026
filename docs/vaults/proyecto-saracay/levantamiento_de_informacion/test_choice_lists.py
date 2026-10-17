import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

res = requests.get(f"{BASE_URL}/api/v2/assets/a2BAHpQdZRvJy7vb8NndDU/", headers=headers)
choices = res.json().get("content", {}).get("choices", [])
list_names = list({c["list_name"] for c in choices})
print("Total lists:", len(list_names))

for lname in list_names:
    sub_choices = [c for c in choices if c["list_name"] == lname]
    survey = [
        {"type": "select_one", "select_from_list_name": lname, "name": f"q_{lname}", "label": f"Pregunta {lname}"}
    ]
    p = {
        "name": f"Test Choice {lname}",
        "asset_type": "survey",
        "content": json.dumps({"schema": "1", "survey": survey, "choices": sub_choices, "settings": {}})
    }
    r = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=p)
    uid = r.json().get("uid")
    rd = requests.post(f"{BASE_URL}/api/v2/assets/{uid}/deployment/", headers=headers_dep, data={"active": "true"})
    print(f"List {lname}: status = {rd.status_code}")
