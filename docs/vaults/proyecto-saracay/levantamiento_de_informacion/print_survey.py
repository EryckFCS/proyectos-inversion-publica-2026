import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

res = requests.get(f"{BASE_URL}/api/v2/assets/a2BAHpQdZRvJy7vb8NndDU/", headers=headers)
content = res.json().get("content", {})
survey = content.get("survey", [])
choices = content.get("choices", [])

for i, q in enumerate(survey):
    print(f"{i}: {q.get('name')} | {q.get('type')} | list: {q.get('select_from_list_name')}")
