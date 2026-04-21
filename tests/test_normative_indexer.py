import asyncio
import json

from scripts import normative_indexer


def test_index_normative_docs_uses_central_memory(monkeypatch, tmp_path):
    metadata_path = tmp_path / "metadata.json"
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    (raw_dir / "documento.pdf").write_bytes(b"%PDF-1.4\n")
    metadata_path.write_text(
        json.dumps(
            {
                "library": [
                    {
                        "id": "DOC1",
                        "name": "Documento de prueba",
                        "path": "documento.pdf",
                        "task_relevance": "Prueba de indexación",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    calls = {}

    class FakeMemory:
        def __init__(self, collection_name):
            self.collection_name = collection_name
            self.persist_path = tmp_path / "central_store"

        def store_many(self, contents, metadatas, collection, doc_ids):
            calls["contents"] = contents
            calls["metadatas"] = metadatas
            calls["collection"] = collection
            calls["doc_ids"] = doc_ids
            return doc_ids

    class FakeProcessor:
        def __init__(self, ocr_enabled):
            self.ocr_enabled = ocr_enabled

        async def extract_text(self, pdf_path):
            return (
                "Primer párrafo con suficiente longitud para pasar el filtro de indexación.\n\n"
                "Segundo párrafo también supera el mínimo requerido para almacenar fragmentos.",
                True,
            )

    monkeypatch.setattr(normative_indexer, "AgentMemory", FakeMemory)
    monkeypatch.setattr(normative_indexer, "PDFProcessor", FakeProcessor)

    asyncio.run(
        normative_indexer.index_normative_docs(
            metadata_path, raw_dir, collection_name="marco_normativo"
        )
    )

    assert calls["contents"] == [
        "Primer párrafo con suficiente longitud para pasar el filtro de indexación.",
        "Segundo párrafo también supera el mínimo requerido para almacenar fragmentos.",
    ]
    assert calls["collection"] == "marco_normativo"
    assert calls["doc_ids"] == ["DOC1_c0", "DOC1_c1"]
    assert calls["metadatas"][0]["source_id"] == "DOC1"
    assert calls["metadatas"][0]["is_ocr"] is True
