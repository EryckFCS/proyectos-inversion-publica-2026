from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

import yaml


class LPIConfig:
    """Configuración canonizada para el nodo Public Investment Projects."""

    _instance: ClassVar[LPIConfig | None] = None
    project_name: str = "Public Investment Projects"
    rag_collection: str = "marco_normativo"

    def __new__(cls) -> LPIConfig:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return

        self.root_path = self._discover_root()
        self.config_path = self.root_path / "config" / "params.yaml"
        self.params: dict[str, Any] = {}
        self.has_config = False
        self.reload()
        self._initialized = True

    def _discover_root(self) -> Path:
        current = Path.cwd().resolve()
        for candidate in (current, *current.parents):
            if (candidate / "pyproject.toml").is_file():
                return candidate
        return current

    def _load_params(self) -> dict[str, Any]:
        if not self.config_path.is_file():
            return {}

        try:
            loaded = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            return {}

        if isinstance(loaded, dict):
            return loaded
        return {}

    def reload(self) -> dict[str, Any]:
        self.params = self._load_params()
        self.has_config = self.config_path.is_file() and bool(self.params)
        return self.params

    def get(self, path: str, default: Any | None = None) -> Any:
        current: Any = self.params
        for key in path.split("."):
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current


NodeSettings = LPIConfig
settings = LPIConfig()
