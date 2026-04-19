import sys
from pathlib import Path
import json
import yaml

# Añadir la ruta de las librerías para el test
sys.path.append("/home/erick-fcs/Capital_Workstation/capital-workstation-libs/src")

from ecs_quantitative.core.audit import LineageEngine
from ecs_quantitative.core.orchestration import BaseOrchestrator

def stress_test_blindaje():
    root = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/public_investment_projects/scratch/mock_project")
    root.mkdir(parents=True, exist_ok=True)
    
    # 1. Test de Catálogo Corrupto
    catalog_corrupto = root / "catalog_bad.yaml"
    with open(catalog_corrupto, "w") as f:
        f.write("datasets: [unclosed_list") # YAML inválido
    
    print("\n--- TEST 1: Catálogo Corrupto ---")
    engine = LineageEngine(root, catalog_corrupto)
    if engine.catalog == {}:
        print("✅ ÉXITO: El motor interceptó el YAML corrupto y devolvió un catálogo vacío de forma segura.")
    else:
        print("❌ FALLO: El motor no manejó el YAML corrupto correctamente.")

    # 2. Test de Integridad Híbrida (Sidecars)
    data_file = root / "test_data.csv"
    with open(data_file, "w") as f: f.write("id,value\n1,100")
    
    # Crear sidecar con hash incorrecto
    sidecar_file = root / "test_data.csv.json"
    with open(sidecar_file, "w") as f:
        json.dump({"input_hash": "sha256:FAKE_HASH_123"}, f)
        
    catalog_valid = root / "catalog_valid.yaml"
    catalog_data = {
        "datasets": {
            "test": {
                "files": [{"id": "D01", "path": "test_data.csv", "sha256": "819077227d853eade7ac21021469e71ed3d82a174092b67f276632c02821a711"}]
            }
        }
    }
    with open(catalog_valid, "w") as f:
        yaml.dump(catalog_data, f)
        
    print("\n--- TEST 2: Integridad Híbrida (Sidecar Mismatch) ---")
    engine_h = LineageEngine(root, catalog_valid)
    files, alerts = engine_h.verify_all()
    
    sidecar_alert = any("Sidecar Mismatch" in a for a in alerts)
    if sidecar_alert:
        print("✅ ÉXITO: El sistema detectó la inconsistencia entre el archivo físico y su sidecar de Pydantic.")
    else:
        print(f"❌ FALLO: No se detectó el error del sidecar. Alertas: {alerts}")

    # 3. Test de Orquestador Forense
    print("\n--- TEST 3: Orquestación Forense ---")
    orch = BaseOrchestrator("Stress_Project", root)
    # Intentar correr un comando que falle
    success, output = orch.run_tests_forensic(["ls", "/directorio/que/no/existe"])
    
    if not success and "STDERR" in output:
        print("✅ ÉXITO: El orquestador capturó la salida de error del subproceso para el reporte JSON.")
        print(f"Detalle capturado: {output.splitlines()[-1]}")
    else:
        print("❌ FALLO: El orquestador no capturó el error correctamente.")

if __name__ == "__main__":
    stress_test_blindaje()
