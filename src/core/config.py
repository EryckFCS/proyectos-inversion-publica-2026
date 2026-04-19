import os
import yaml
from pathlib import Path


class LPIConfig:
    """
    Gestor de configuración central del Laboratorio de Proyectos de Inversión (LPI).
    Localiza la raíz del proyecto y carga los parámetros desdeparams.yaml.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LPIConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Detectar la raíz del proyecto (la carpeta que contiene pyproject.toml o .git)
        self.root_path = self._find_project_root()
        self.config_path = self.root_path / "config" / "params.yaml"

        self.params = {}
        self.load_config()
        self._initialized = True

    def _find_project_root(self):
        """Busca el archivo pyproject.toml hacia arriba para encontrar la raíz."""
        current = Path(os.getcwd()).absolute()
        for parent in [current] + list(current.parents):
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                return parent
        # Si no se encuentra, asumir el directorio actual
        return current

    def load_config(self):
        """Carga el archivo YAML de parámetros."""
        if not self.config_path.exists():
            print(
                f"⚠️ Advertencia: No se encontró el archivo de configuración en {self.config_path}"
            )
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.params = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error al cargar la configuración: {e}")

    def get(self, key_path, default=None):
        """
        Obtiene un valor usando una ruta de puntos (ej. 'evaluacion_social.tasa_social_descuento').
        """
        keys = key_path.split(".")
        value = self.params
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value


# Instancia única para exportar
lpi_settings = LPIConfig()
