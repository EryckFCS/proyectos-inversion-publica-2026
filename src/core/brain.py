import sys
from pathlib import Path

# La ruta central es compartida por todos los nodos de la federación
CENTRAL_BRAIN_PATH = Path("~/.capital/brain/vector_store").expanduser()

try:
    from ecs_quantitative.memory.agent_memory import AgentMemory
except ImportError:
    AgentMemory = None


class LaboratorioBrain:
    """
    Consumidor del Motor RAG Central.
    Accede al conocimiento semántico federado en la estación de trabajo.
    """

    def __init__(self, collection="pip_marco_normativo"):
        self.persist_path = CENTRAL_BRAIN_PATH
        self.collection = collection

        if AgentMemory:
            self.memory = AgentMemory(
                persist_path=self.persist_path, collection_name=self.collection
            )
        else:
            self.memory = None
            print("⚠️ Advertencia: Memoria Central no disponible.")

    def search(self, query, top_n=3):
        """Realiza una búsqueda semántica federada."""
        if not self.memory:
            return []
        
        return self.memory.recall(
            query=query, n_results=top_n, collection=self.collection
        )

    def get_context(self, query, top_n=3):
        """Genera un bloque de contexto institucional para reportes."""
        results = self.search(query, top_n)
        if not results:
            return "No se encontró información relevante en el cerebro central."

        context = "### Contexto Recuperado (Memoria Central Federada):\n\n"
        for i, res in enumerate(results):
            meta = res.get("metadata", {})
            source = meta.get("source_name", "Fuente Central")
            content = res.get("content", "")
            context += f"**Fragmento {i + 1} | {source}**\n> {content}\n\n"

        return context


# Instancia global configurada para PIP
brain_engine = LaboratorioBrain()
