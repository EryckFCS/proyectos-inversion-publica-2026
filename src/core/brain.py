import sys
from pathlib import Path
from src.core.config import lpi_settings

# Asegurar descubrimiento de librerías externas de la estación de trabajo
LIBS_PATH = Path("/home/erick-fcs/Capital_Workstation/capital-workstation-libs")
if str(LIBS_PATH) not in sys.path:
    sys.path.append(str(LIBS_PATH))

try:
    from ecs_quantitative.memory.agent_memory import AgentMemory
except ImportError:
    # Fallback o manejo de error si no está disponible
    AgentMemory = None


class LaboratorioBrain:
    """
    Motor RAG (Retrieval-Augmented Generation) centralizado.
    Gestiona el conocimiento semántico del laboratorio.
    """

    def __init__(self, collection="marco_normativo"):
        self.persist_path = (
            lpi_settings.root_path / "data" / "processed" / "vector_store"
        )
        self.collection = collection

        if AgentMemory:
            self.memory = AgentMemory(
                persist_path=self.persist_path, collection_name=self.collection
            )
        else:
            self.memory = None
            print("⚠️ Advertencia: Librería 'ecs_quantitative' no disponible.")

    def search(self, query, top_n=3):
        """Realiza una búsqueda semántica y retorna fragmentos relevantes."""
        if not self.memory:
            return []

        # El método correcto en esta versión de la lib es 'recall'
        results = self.memory.recall(
            query=query, n_results=top_n, collection=self.collection
        )
        return results

    def get_context(self, query, top_n=3):
        """Genera un bloque de contexto formateado para un prompt o reporte."""
        results = self.search(query, top_n)

        if not results:
            return "No se encontró información relevante en el cerebro."

        context = "### Contexto Recuperado (Segundo Cerebro LPI):\n\n"

        # Estructura de resultados de recall: Lista de dicts con 'content' y 'metadata'
        if isinstance(results, list):
            for i, res in enumerate(results):
                meta = res.get("metadata", {})
                source = meta.get("source_name", "Fuente desconocida")
                content = res.get("content", "")
                context += f"**Fragmento {i + 1} | {source}**\n"
                context += f"> {content}\n\n"

        return context


# Instancia global
brain_engine = LaboratorioBrain()
