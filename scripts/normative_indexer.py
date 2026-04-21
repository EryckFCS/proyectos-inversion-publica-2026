import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from ecs_quantitative.ingestion.processors.pdf import PDFProcessor
from ecs_quantitative.memory.agent_memory import AgentMemory


def chunk_text(text: str, min_length: int = 40) -> list[str]:
    """Divide el texto normativo en fragmentos útiles para indexación."""
    return [chunk.strip() for chunk in text.split("\n\n") if len(chunk.strip()) > min_length]


def build_chunk_metadata(item: dict[str, Any], chunk_index: int, is_ocr: bool) -> dict[str, Any]:
    """Construye metadatos estables para cada fragmento indexado."""
    return {
        "source_id": item["id"],
        "source_name": item["name"],
        "chunk_index": chunk_index,
        "is_ocr": is_ocr,
        "type": "normative_text",
        "relevance": item.get("task_relevance", ""),
    }


async def index_normative_docs(metadata_path, base_raw_dir, collection_name="marco_normativo"):
    memory = AgentMemory(collection_name=collection_name)
    processor = PDFProcessor(ocr_enabled=True)

    with open(metadata_path, "r", encoding="utf-8") as handle:
        metadata = json.load(handle)

    for item in metadata.get("library", []):
        pdf_path = Path(base_raw_dir) / item["path"]
        if not pdf_path.exists():
            print(f"File not found: {pdf_path}")
            continue

        print(f"Processing and indexing: {item['name']} ({item['id']})...")
        text, is_ocr = await processor.extract_text(pdf_path)
        chunks = chunk_text(text or "")

        if not chunks:
            print(f"  No se encontraron fragmentos indexables en {item['id']}.")
            continue

        print(f"  Found {len(chunks)} chunks. Storing in central memory...")
        metadatas = [build_chunk_metadata(item, idx, is_ocr) for idx in range(len(chunks))]
        doc_ids = [f"{item['id']}_c{idx}" for idx in range(len(chunks))]
        memory.store_many(
            contents=chunks,
            metadatas=metadatas,
            collection=collection_name,
            doc_ids=doc_ids,
        )

    print(f"SUCCESS: Marco Normativo indexed in {collection_name} collection.")
    print(f"Location: {memory.persist_path}")


if __name__ == "__main__":
    meta_p = Path("data/raw/marco_normativo/metadata.json")
    raw_d = Path("data/raw/marco_normativo")

    if not meta_p.exists():
        print(f"Metadata not found at {meta_p}. Please check paths.")
        sys.exit(1)

    asyncio.run(index_normative_docs(meta_p, raw_d))
