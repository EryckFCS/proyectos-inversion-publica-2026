"""
check_rag_marco_normativo.py
Diagnóstico del lóbulo `marco_normativo` para el nodo PIP.
Verifica qué documentos están indexados y cuántos chunks tiene cada fuente.
"""
import chromadb
from pathlib import Path
from loguru import logger

VECTOR_STORE = Path.home() / ".capital" / "brain" / "vector_store"


def check():
    client = chromadb.PersistentClient(path=str(VECTOR_STORE))

    try:
        col = client.get_collection("marco_normativo")
    except Exception as e:
        logger.error(f"Colección 'marco_normativo' no encontrada: {e}")
        return

    total = col.count()
    logger.info(f"Colección 'marco_normativo': {total} chunks totales")

    # Muestrear metadatos para ver qué documentos están indexados
    sample = col.get(limit=total, include=["metadatas"])
    sources: dict[str, int] = {}
    for meta in sample.get("metadatas", []):
        src = meta.get("source", meta.get("file_name", "desconocido"))
        sources[src] = sources.get(src, 0) + 1

    logger.info(f"Documentos indexados ({len(sources)}):")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        logger.info(f"  {count:>5} chunks — {src}")


if __name__ == "__main__":
    check()
