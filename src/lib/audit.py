from src.core.lineage import lineage_engine
from datetime import datetime


def generate_report_audit_summary(file_ids):
    """
    Genera un bloque de texto formateado para auditoría en reportes Quarto.
    """
    audit_data = lineage_engine.get_audit_trail(file_ids)

    total = len(audit_data)
    verified = sum(1 for a in audit_data if a["verified"])
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    summary = "**Certificado de Integridad LPI v4.0**\n\n"
    summary += f"- **Fecha de Auditoría**: {date_now}\n"
    summary += f"- **Fuentes Verificadas**: {verified}/{total}\n"

    if verified == total:
        summary += "- **Estado de Datos**: 🟢 ÍNTEGRO (100% Coincidencia SHA256)\n"
    else:
        summary += "- **Estado de Datos**: 🔴 ALERTA (Inconsistencias detectadas)\n"

    return summary
