import sys
from pathlib import Path
from ecs_quantitative.memory.agent_memory import AgentMemory

def query_article(query_text, collection="marco_normativo", n=1):
    """
    Consulta rápida al Vector Store para recuperar fragmentos normativos.
    """
    persist_path = Path("data/processed/vector_store")
    if not persist_path.exists():
        return "Error: Base de datos RAG no encontrada. Ejecuta indexer primero."
        
    try:
        memory = AgentMemory(persist_path=persist_path, collection_name=collection)
        results = memory.recall(query=query_text, n_results=n, collection=collection)
        
        if not results:
            return f"No se encontró información para: {query_text}"
            
        output = []
        for res in results:
            source = res['metadata'].get('source_id', 'Unknown')
            content = res['content']
            output.append(f"--- [FUENTE: {source}] ---\n{content}")
            
        return "\n\n".join(output)
    except Exception as e:
        return f"Error en consulta RAG: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/normative_query.py 'término o artículo'")
        sys.exit(1)
        
    search_term = sys.argv[1]
    print(query_article(search_term))
