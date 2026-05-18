from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

import yaml
from ecs_quantitative.core.federation import FederatedNodeConfig


class LPIConfig(FederatedNodeConfig):
    """Configuración canonizada para el nodo Public Investment Projects."""

    _instance: ClassVar[LPIConfig | None] = None
    project_name: str = "Public Investment Projects"
    rag_collection: str = "marco_normativo"

    def __new__(cls) -> LPIConfig:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, **values: Any) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__(**values)
        self.params: dict[str, Any] = {}
        self.has_config = False
        self.reload()
        self._initialized = True

    def reload(self) -> dict[str, Any]:
        params_path = self.root_path / "config" / "params.yaml"
        if params_path.is_file():
            try:
                self.params = yaml.safe_load(params_path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                self.params = {}
        else:
            self.params = {}
        self.has_config = params_path.is_file() and bool(self.params)
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

