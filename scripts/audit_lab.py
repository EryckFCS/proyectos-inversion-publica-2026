from pathlib import Path

import ecs_quantitative
from ecs_quantitative.audit.engine import AuditEngine

# Rutas de la infraestructura federada
LIBS_SRC = Path(ecs_quantitative.__file__).resolve().parent
PROJECT_ROOT = Path(__file__).parent.parent


def run_central_audit():
    print("🛡️ Auditoría de Gobernanza Federada v7.4.0")
    print("=" * 50)

    if not LIBS_SRC.exists():
        print(f"❌ Error: No se encontró la fuente de la librería central en {LIBS_SRC}")
        return

    # 1. Inicializar motor central
    engine = AuditEngine(core_dir=LIBS_SRC)

    # 2. Auditar este nodo (PIP)
    print(f"🔍 Analizando nodo: {PROJECT_ROOT.name}...")
    stats = engine.audit_project(PROJECT_ROOT)

    # 3. Reportar resultados
    print("\n📊 Resultados de Auditoría:")
    print(f"  - Archivos analizados: {stats['files']}")
    print(f"  - Líneas de código (LOC): {stats['loc']}")
    print(f"  - Estado del ciclo de vida: {stats['lifecycle']}")

    if stats["redundancies"]:
        print("\n⚠️  REDUNDANCIAS DETECTADAS (Candidatos a migración central):")
        for r in stats["redundancies"]:
            print(f"  [-] {r}")

    if stats["hardcoded_paths"]:
        print("\n🚨 RUTAS HARDCODED DETECTADAS (Riesgo de portabilidad):")
        for p in stats["hardcoded_paths"]:
            print(f"  [!] {p}")

    print("\n" + "=" * 50)
    print("✨ Auditoría completada. Consulta AGENTS.md para más detalles de gobernanza.")


if __name__ == "__main__":
    run_central_audit()
