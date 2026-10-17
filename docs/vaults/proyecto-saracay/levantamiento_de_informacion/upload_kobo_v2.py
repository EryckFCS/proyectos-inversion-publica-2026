import requests
import json

token = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
headers = {"Authorization": f"Token {token}"}
file_path = r"d:\07_Ciclo\septimo_ciclo\public_investment_projects\docs\vaults\proyecto-saracay\levantamiento_de_informacion\encuesta_diagnostico_saracay_kobo_v2.xlsx"

print("Subiendo encuesta_diagnostico_saracay_kobo_v2.xlsx a KoboToolbox...")
with open(file_path, "rb") as f:
    files = {"file": f}
    res = requests.post(
        "https://kf.kobotoolbox.org/api/v2/imports/",
        headers=headers,
        files=files,
        data={"name": "Diagnóstico Territorial y Saneamiento Básico - Parroquia Saracay"}
    )
    print("Respuesta Import:", res.status_code, res.text)
