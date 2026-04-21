import sys
from ecs_quantitative.memory.agent_memory import AgentMemory


def query_article(query_text, collection="marco_normativo", n=1):
    """
    Consulta rápida al Vector Store CENTRAL para recuperar fragmentos normativos.
    """
    try:
        # AgentMemory usa automáticamente ~/.capital/brain/vector_store
        memory = AgentMemory(collection_name=collection)
        results = memory.recall(query=query_text, n_results=n, collection=collection)

        if not results:
            return f"No se encontró información para: {query_text} en la memoria central."

        output = []
        for res in results:
            meta = res.get("metadata", {})
            source = meta.get("source_name", meta.get("source_id", "Unknown"))
            content = res["content"]
            output.append(f"--- [FUENTE CENTRAL: {source}] ---\n{content}")

        return "\n\n".join(output)
    except Exception as e:
        return f"❌ Error en consulta RAG Central: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/normative_query.py 'término o artículo'")
        sys.exit(1)

    search_term = sys.argv[1]
    print(query_article(search_term))
