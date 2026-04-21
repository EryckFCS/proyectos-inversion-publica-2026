import asyncio

from scripts import sync_brain


def test_sync_knowledge_indexes_pdf_into_central_memory(monkeypatch, tmp_path):
    project_root = tmp_path
    sources_dir = project_root / "data" / "raw" / "marco_normativo"
    sources_dir.mkdir(parents=True)
    (sources_dir / "doc.pdf").write_bytes(b"%PDF-1.4\n")

    calls = {"stores": [], "deletes": []}

    class FakeCollection:
        def delete(self, where):
            calls["deletes"].append(where)

    class FakeClient:
        def get_collection(self, name):
            assert name == "marco_normativo"
            return FakeCollection()

    class FakeMemory:
        def __init__(self, collection_name):
            self.collection_name = collection_name
            self.client = FakeClient()

        def store(self, content, metadata, doc_id, collection):
            calls["stores"].append(
                {
                    "content": content,
                    "metadata": metadata,
                    "doc_id": doc_id,
                    "collection": collection,
                }
            )

    class FakeProcessor:
        def __init__(self, ocr_enabled):
            self.ocr_enabled = ocr_enabled

        async def extract_text(self, pdf_path):
            return (
                "Primer bloque con suficiente longitud para ser indexado correctamente.\n\n"
                "Segundo bloque con suficiente longitud para ser indexado correctamente.",
                False,
            )

    class FakeAuditEngine:
        def __init__(self, core_dir):
            self.core_dir = core_dir

    monkeypatch.setattr(sync_brain, "PROJECT_ROOT", project_root)
    monkeypatch.setattr(sync_brain, "LIBS_SRC", project_root / "central_src")
    monkeypatch.setattr(sync_brain, "AgentMemory", FakeMemory)
    monkeypatch.setattr(sync_brain, "PDFProcessor", FakeProcessor)

    asyncio.run(sync_brain.sync_knowledge())

    assert calls["deletes"] == [{"source_id": "doc"}]
    assert [entry["doc_id"] for entry in calls["stores"]] == ["doc_0", "doc_1"]
    assert calls["stores"][0]["collection"] == "marco_normativo"
    assert calls["stores"][0]["metadata"]["source_id"] == "doc"
