from __future__ import annotations

from typing import Any

from ecs_quantitative.memory.agent_memory import AgentMemory

from .config import settings


class LaboratorioBrain:
    """Wrapper local del cerebro del nodo PIP."""

    def __init__(
        self,
        collection: str | None = None,
        config: Any | None = None,
        memory: Any | None = None,
    ) -> None:
        self.config = config if config is not None else settings
        self.collection = collection or getattr(self.config, "rag_collection", "marco_normativo")
        self.connection_error: str | None = None

        if memory is not None:
            self.memory = memory
            self.is_available = True
            return

        try:
            self.memory = AgentMemory(collection_name=self.collection)
            self.is_available = True
        except Exception as exc:
            self.memory = None
            self.connection_error = str(exc)
            self.is_available = False

    def search(self, topic: str, top_n: int = 2) -> list[dict[str, Any]]:
        if self.memory is None:
            return []

        try:
            return self.memory.recall(query=topic, n_results=top_n, collection=self.collection)
        except Exception as exc:
            self.connection_error = str(exc)
            self.is_available = False
            return []

    def get_context(self, question: str, top_n: int = 3) -> str:
        results = self.search(question, top_n=top_n)
        if not results:
            return "No se encontró información relevante en el cerebro central."

        lines = ["Contexto Recuperado"]
        for item in results:
            if not isinstance(item, dict):
                continue
            metadata = item.get("metadata", {})
            source = metadata.get("source_name", metadata.get("source_id", "Fuente"))
            content = item.get("content", "")
            lines.append(f"- {content} ({source})")

        return "\n".join(lines)


NodeBrain = LaboratorioBrain
brain_engine = LaboratorioBrain(config=settings)
brain = brain_engine
