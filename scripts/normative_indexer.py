import sys
from pathlib import Path
import json
import asyncio

# The libraries should be available in the environment created by uv
try:
    from ecs_quantitative.memory.agent_memory import AgentMemory
    from ecs_quantitative.ingestion.processors.pdf import PDFProcessor
except ImportError as e:
    print(f"Error: {e}")
    print("Ensure 'capital-workstation-libs' is properly linked.")
    sys.exit(1)


async def index_normative_docs(
    metadata_path, base_raw_dir, collection_name="marco_normativo"
):
    # Target directory for ChromaDB within the project
    persist_path = Path("data/processed/vector_store")

    print(f"Initializing ChromaDB at {persist_path}...")
    memory = AgentMemory(persist_path=persist_path, collection_name=collection_name)

    # PDF Processor with OCR enabled for potential low-quality scans
    processor = PDFProcessor(ocr_enabled=True)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    for item in metadata.get("library", []):
        pdf_path = Path(base_raw_dir) / item["path"]
        if not pdf_path.exists():
            print(f"File not found: {pdf_path}")
            continue

        print(f"Processing and indexing: {item['name']} ({item['id']})...")
        text, is_ocr = await processor.extract_text(pdf_path)

        # Simple heuristic chunking for normative text
        # Splitting by double newline usually separates articles or paragraphs
        raw_chunks = text.split("\n\n")
        chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 40]

        print(f"  Found {len(chunks)} chunks. Storing in ChromaDB...")

        for idx, chunk in enumerate(chunks):
            meta = {
                "source_id": item["id"],
                "source_name": item["name"],
                "chunk_index": idx,
                "is_ocr": is_ocr,
                "type": "normative_text",
                "relevance": item.get("task_relevance", ""),
            }
            memory.store(
                content=chunk,
                metadata=meta,
                collection=collection_name,
                doc_id=f"{item['id']}_c{idx}",
            )

    print(f"SUCCESS: Marco Normativo indexed in {collection_name} collection.")
    print(f"Location: {persist_path}")


if __name__ == "__main__":
    meta_p = "data/raw/marco_normativo/metadata.json"
    raw_d = "data/raw/marco_normativo"

    if not Path(meta_p).exists():
        print(f"Metadata not found at {meta_p}. Please check paths.")
        sys.exit(1)

    asyncio.run(index_normative_docs(meta_p, raw_d))
