import hashlib
import yaml
from src.core.config import lpi_settings


class LineageManager:
    """
    Gestiona el linaje y la integridad forense de los datos del laboratorio.
    Verifica que los archivos físicos coincidan con el catálogo maestro.
    """

    def __init__(self):
        self.root_path = lpi_settings.root_path
        self.catalog_path = self.root_path / "config" / "data_catalog.yaml"
        self.catalog = self._load_catalog()

    def _load_catalog(self):
        """Carga el catálogo de datos YAML."""
        if not self.catalog_path.exists():
            return {}
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def calculate_sha256(self, file_path):
        """Calcula el hash SHA256 de un archivo."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Leer en bloques para manejar archivos grandes
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return None

    def verify_file(self, file_id):
        """
        Verifica la integridad de un archivo específico por su ID.
        Retorna (status, message).
        """
        # Buscar el archivo en el catálogo
        target_file = None
        for category in self.catalog.get("datasets", {}).values():
            for f in category.get("files", []):
                if f["id"] == file_id:
                    target_file = f
                    break

        if not target_file:
            return False, f"ID de archivo '{file_id}' no encontrado en el catálogo."

        full_path = self.root_path / target_file["path"]
        if not full_path.exists():
            return (
                False,
                f"ERROR: Archivo físico no encontrado en {target_file['path']}",
            )

        current_hash = self.calculate_sha256(full_path)
        expected_hash = target_file.get("sha256")

        if current_hash == expected_hash:
            return True, f"VERIFICADO: {target_file['name']} íntegro."
        else:
            return (
                False,
                f"¡ALERTA!: {target_file['name']} ha sido alterado o está corrupto.",
            )

    def get_audit_trail(self, file_ids):
        """Genera un resumen de auditoría para una lista de archivos."""
        trail = []
        for fid in file_ids:
            status, msg = self.verify_file(fid)
            trail.append({"id": fid, "verified": status, "detail": msg})
        return trail

    def get_verified_files(self):
        """
        Retorna una lista de diccionarios con la información de todos los
        archivos que pasan la prueba de integridad.
        """
        verified_list = []
        for category in self.catalog.get("datasets", {}).values():
            for f in category.get("files", []):
                status, _ = self.verify_file(f["id"])
                if status:
                    # Clonar para no modificar el original
                    file_data = f.copy()
                    file_data["full_path"] = self.root_path / f["path"]
                    verified_list.append(file_data)
        return verified_list


# Instancia global
lineage_engine = LineageManager()
