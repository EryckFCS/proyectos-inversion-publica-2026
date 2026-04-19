from ecs_quantitative.core.audit import LineageEngine
from src.core.config import lpi_settings

class LineageManager(LineageEngine):
    """
    Nodo de Linaje para el laboratorio PIP.
    Implementación soberana que utiliza el motor universal ecs_quantitative.
    """
    def __init__(self):
        root = lpi_settings.root_path
        catalog = root / "config" / "data_catalog.yaml"
        super().__init__(root_path=root, catalog_path=catalog)

    def get_audit_trail(self, file_ids):
        """Simplificación compatible con la versión anterior."""
        verified, alerts = self.verify_all()
        # Filtrar solo los solicitados (mantenimiento de compatibilidad)
        trail = []
        for fid in file_ids:
            # En el motor universal f['id'] está disponible en el dict de verified
            found = next((f for f in verified if f["id"] == fid), None)
            if found:
                trail.append({"id": fid, "verified": True, "detail": "VERIFICADO"})
            else:
                trail.append({"id": fid, "verified": False, "detail": "ALERTA/MISSING"})
        return trail

    def get_verified_files(self):
        """Redirección al motor universal."""
        verified, _ = self.verify_all()
        return verified
    
    def heal_catalog(self):
        """Redirección al motor universal."""
        return self.heal()


# Instancia global
lineage_engine = LineageManager()
