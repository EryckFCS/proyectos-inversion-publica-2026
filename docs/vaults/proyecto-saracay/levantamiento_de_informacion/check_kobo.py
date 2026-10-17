import urllib.request
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}"}

req = urllib.request.Request("https://kf.kobotoolbox.org/api/v2/assets/", headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"Total assets: {data.get('count', 0)}")
        for item in data.get("results", []):
            uid = item.get("uid")
            name = item.get("name")
            deployed = item.get("has_deployment")
            print(f"UID: {uid} | Name: {name} | Deployed: {deployed}")
except Exception as e:
    print("Error:", e)
