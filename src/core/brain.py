from ecs_quantitative.memory.agent_memory import AgentMemory


class LaboratorioBrain:
    """
    Consumidor del Motor RAG Central.
    Accede al conocimiento semántico federado en la estación de trabajo.
    """

    def __init__(self, collection="marco_normativo"):
        # AgentMemory usa por defecto ~/.capital/brain/vector_store
        self.collection = collection
        try:
            self.memory = AgentMemory(collection_name=self.collection)
        except Exception as e:
            self.memory = None
            print(f"⚠️ Error al conectar con la Memoria Central: {e}")

    def search(self, query, top_n=3):
        """Realiza una búsqueda semántica federada."""
        if not self.memory:
            return []

        return self.memory.recall(query=query, n_results=top_n, collection=self.collection)

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
