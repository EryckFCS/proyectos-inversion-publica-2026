import sys
from pathlib import Path
from ecs_quantitative.core.orchestration import BaseOrchestrator

# Asegurar descubrimiento de src para tests locales
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.core.lineage import lineage_engine

class PIPOrchestrator(BaseOrchestrator):
    """
    Orquestador específico para Proyectos de Inversión Pública (PIP).
    Hereda la infraestructura de inmunidad global de ecs_quantitative.
    """
    def __init__(self):
        super().__init__(project_name="LPI-PIP", project_root=project_root)

    def run_health_check(self):
        print(f"🚀 {self.project_name} Orchestrator: Ejecutando protocolo industrial v2.0...")
        
        status = {
            "layers": {
                "core_integrity": False,
                "logic_validation": False,
                "environment": False,
                "academic_compliance": False
            },
            "alerts": [],
            "academic_stats": {},
            "forensic_details": {}
        }

        # 1. Integridad (Híbrida: YAML + Sidecars)
        verified_files, integrity_alerts = lineage_engine.verify_all()
        total_catalog = sum(len(cat.get("files", [])) for cat in lineage_engine.catalog.get("datasets", {}).values())
        
        status["layers"]["core_integrity"] = (len(verified_files) == total_catalog)
        status["alerts"].extend(integrity_alerts)

        # 2. Lógica (Forense: Pytest con captura de logs)
        test_success, test_logs = self.run_tests_forensic(["pytest", "tests/test_evaluacion.py"])
        status["layers"]["logic_validation"] = test_success
        if not test_success:
            status["alerts"].append("FALLO_LÓGICO: Las pruebas de evaluación han fallado.")
            status["forensic_details"]["logic_error"] = test_logs

        # 3. Gobernanza Académica (Garantía de Evidencias)
        # Definimos las unidades específicas de PIP según la estructura detectada
        pip_units = {
            "U1": "Diagnostico-y-Analisis",
            "U2": "Marco-Logico",
            "U3": "Seguimiento-Evaluacion"
        }
        aca_stats, aca_alerts = self.run_academic_check(subject_code="PIP", custom_units=pip_units)
        status["academic_stats"] = aca_stats
        status["alerts"].extend(aca_alerts)
        status["layers"]["academic_compliance"] = (len(aca_alerts) == 0)

        # 4. Entorno
        tool_status, env_alerts = self.check_environment(["quarto", "python", "uv"])
        status["layers"]["environment"] = all(tool_status.values())
        status["alerts"].extend(env_alerts)

        self.generate_report(status)
        return status

    def auto_heal(self):
        print("🔧 Iniciando auto-curación federada...")
        if lineage_engine.heal():
            print("✨ Catálogo sincronizado.")
        return self.run_health_check()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--heal", action="store_true")
    args = parser.parse_args()

    orchestrator = PIPOrchestrator()
    if args.heal:
        orchestrator.auto_heal()
    else:
        orchestrator.run_health_check()
