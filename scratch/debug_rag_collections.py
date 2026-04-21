"""
Script de Diagnóstico RAG: Listar Colecciones
Verifica qué colecciones están disponibles en el cerebro central.
"""

from pathlib import Path
import chromadb


def list_central_collections():
    central_path = Path("~/.capital/brain/vector_store").expanduser()

    if not central_path.exists():
        print(f"❌ La ruta central no existe: {central_path}")
        return

    print(f"🔍 Conectando a Chroma en: {central_path}")
    client = chromadb.PersistentClient(path=str(central_path))

    collections = client.list_collections()

    if not collections:
        print("⚠️ No se encontraron colecciones en este persistent store.")
    else:
        print(f"\n✅ Encontradas {len(collections)} colecciones:")
        for coll in collections:
            count = coll.count()
            print(f"- **Nombre**: {coll.name} | **Documentos**: {count}")


if __name__ == "__main__":
    list_central_collections()
