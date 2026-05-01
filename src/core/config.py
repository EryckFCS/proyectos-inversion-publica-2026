from __future__ import annotations
from ecs_quantitative.core.federation import FederatedNodeConfig

class NodeSettings(FederatedNodeConfig):
    """Configuración canonizada para el nodo public_investment_projects."""
    project_name: str = "Public Investment Projects"
    rag_collection: str = "public_investment_projects"

settings = NodeSettings()
