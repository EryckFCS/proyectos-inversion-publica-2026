import requests
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
asset_uid = "aDrLC6UgnmU2q4VS8b8M4t"
version_id = "vyTZqphnBB8nFdv5TSsaV5"

# Probar PATCH directamente sobre el asset
res_patch = requests.patch(
    f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/",
    headers=headers,
    json={"deployment__active": True}
)
print("Patch asset deployment__active:", res_patch.status_code)

# Probar POST con payload
res_post = requests.post(
    f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/deployment/",
    headers=headers,
    json={"active": True}
)
print("Deploy POST with active:True:", res_post.status_code)

res_info = requests.get(f"https://kf.kobotoolbox.org/api/v2/assets/{asset_uid}/", headers=headers)
print("Deployment links:", res_info.json().get("deployment__links"))
print("Has deployment:", res_info.json().get("has_deployment"))
