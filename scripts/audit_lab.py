import sys
from pathlib import Path

# Asegurar descubrimiento de src
sys.path.append(str(Path(__file__).parent.parent))

from src.core.lineage import lineage_engine


def audit_all():
    print("🛡️ Auditoría Forense LPI v4.0")
    print("=" * 50)

    catalog = lineage_engine.catalog
    all_files = []

    for category_name, category_data in catalog.get("datasets", {}).items():
        print(f"\n📁 Categoría: {category_name}")
        for f in category_data.get("files", []):
            status, msg = lineage_engine.verify_file(f["id"])
            icon = "✅" if status else "❌"
            print(f"  {icon} {f['name']:<40} | {msg}")
            all_files.append(status)

    print("\n" + "=" * 50)
    if all(all_files):
        print("🎉 ESTADO: LABORATORIO ÍNTEGRO. No se detectan alteraciones.")
    else:
        print("⚠️ ALERTA: Se han detectado inconsistencias en los datos.")


if __name__ == "__main__":
    audit_all()
