"""
Prueba de Validación RAG Centralizado (Cross-Node Search)
Verifica que el conocimiento de PIP es accesible desde el cerebro central.
"""

from pathlib import Path
from ecs_quantitative.memory.agent_memory import AgentMemory


def test_central_brain():
    central_path = Path("~/.capital/brain/vector_store").expanduser()
    collection = "marco_normativo"

    print(f"🔍 Conectando al Cerebro Central en: {central_path}")
    print(f"📚 Buscando en la colección migrada: {collection}")

    try:
        memory = AgentMemory(persist_path=central_path, collection_name=collection)

        # Realizamos una consulta sobre temas típicos de Proyectos de Inversión (Marco Normativo)
        query = "metodologia de evaluacion social de proyectos invesion publica"
        results = memory.recall(query=query, n_results=3, collection=collection)

        if results:
            print(f"\n✅ ÉXITO: Se recuperaron {len(results)} fragmentos del cerebro central.")
            for i, res in enumerate(results):
                source = res.get("metadata", {}).get("source_name", "Desconocida")
                print(f"\n--- Fragmento {i + 1} | Origen: {source} ---")
                print(f"{res.get('content', '')[:300]}...")
        else:
            print("\n⚠️ AVISO: El cerebro respondió pero no encontró fragmentos para esta consulta.")

    except Exception as e:
        print(f"\n❌ ERROR de acceso al cerebro central: {e}")


if __name__ == "__main__":
    test_central_brain()
