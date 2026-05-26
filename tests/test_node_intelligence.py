"""Consolidated Node Intelligence tests (Config, Brain, RAG query, Indexing, and cleanups)."""

from __future__ import annotations

import json
import asyncio
from pathlib import Path
import pytest

# Config
from src.core.config import LPIConfig
import src.core.brain as brain_module
from scripts import sync_brain
from scripts import normative_indexer
from scripts import normative_query
from src.lib import research as research_module
from scripts.cleanup_guide import clean_guide


# --- LPIConfig Tests ---

def test_lpi_config_loads_from_project_root(monkeypatch, tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "params.yaml").write_text(
        "evaluacion_social:\n"
        "  tasa_social_descuento: 0.12\n"
        "  factores_correccion:\n"
        "    mano_obra_no_calificada: 0.65\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    LPIConfig._instance = None

    config = LPIConfig()

    assert config.root_path == tmp_path
    assert config.get("evaluacion_social.tasa_social_descuento") == 0.12
    assert config.get("evaluacion_social.factores_correccion.mano_obra_no_calificada") == 0.65
    assert config.get("ruta.inexistente", default="fallback") == "fallback"


# --- LaboratorioBrain RAG Exocortex Tests ---

def test_laboratorio_brain_search_and_context(monkeypatch):
    calls = []

    class FakeMemory:
        def __init__(self, collection_name):
            self.collection_name = collection_name

        def recall(self, query, n_results, collection):
            calls.append((query, n_results, collection))
            return [
                {
                    "content": "La planificación pública exige sustento normativo.",
                    "metadata": {"source_name": "Constitución"},
                }
            ]

    monkeypatch.setattr(brain_module, "AgentMemory", FakeMemory)

    brain = brain_module.LaboratorioBrain(collection="marco_normativo")
    results = brain.search("planificación", top_n=2)

    assert calls == [("planificación", 2, "marco_normativo")]
    assert results[0]["content"] == "La planificación pública exige sustento normativo."

    context = brain.get_context("planificación", top_n=2)
    assert "Contexto Recuperado" in context
    assert "Constitución" in context
    assert "La planificación pública exige sustento normativo." in context


def test_laboratorio_brain_handles_memory_failure(monkeypatch):
    class FailingMemory:
        def __init__(self, collection_name):
            raise RuntimeError("memoria no disponible")

    monkeypatch.setattr(brain_module, "AgentMemory", FailingMemory)

    brain = brain_module.LaboratorioBrain()

    assert brain.memory is None
    assert brain.search("consulta") == []
    assert (
        brain.get_context("consulta")
        == "No se encontró información relevante en el cerebro central."
    )


# --- Sync Knowledge Brain Script Tests ---

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

    class FakeMemorySync:
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

    class FakeProcessorSync:
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
    monkeypatch.setattr(sync_brain, "AgentMemory", FakeMemorySync)
    monkeypatch.setattr(sync_brain, "PDFProcessor", FakeProcessorSync)

    asyncio.run(sync_brain.sync_knowledge())

    assert calls["deletes"] == [{"source_id": "doc"}]
    assert [entry["doc_id"] for entry in calls["stores"]] == ["doc_0", "doc_1"]
    assert calls["stores"][0]["collection"] == "marco_normativo"
    assert calls["stores"][0]["metadata"]["source_id"] == "doc"


# --- Normative Indexer Tests ---

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

    class FakeMemoryIndex:
        def __init__(self, collection_name):
            self.collection_name = collection_name
            self.persist_path = tmp_path / "central_store"

        def store_many(self, contents, metadatas, collection, doc_ids):
            calls["contents"] = contents
            calls["metadatas"] = metadatas
            calls["collection"] = collection
            calls["doc_ids"] = doc_ids
            return doc_ids

    class FakeProcessorIndex:
        def __init__(self, ocr_enabled):
            self.ocr_enabled = ocr_enabled

        async def extract_text(self, pdf_path):
            return (
                "Primer párrafo con suficiente longitud para pasar el filtro de indexación.\n\n"
                "Segundo párrafo también supera el mínimo requerido para almacenar fragmentos.",
                True,
            )

    monkeypatch.setattr(normative_indexer, "AgentMemory", FakeMemoryIndex)
    monkeypatch.setattr(normative_indexer, "PDFProcessor", FakeProcessorIndex)

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


# --- RAG Query Engine Tests ---

def test_query_article_no_store():
    """Verifica que el sistema maneje la ausencia de la base de datos."""
    class FailingMemoryQuery:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("memoria no disponible")

    normative_query.AgentMemory = FailingMemoryQuery

    result = normative_query.query_article("test query", collection="non_existent_collection")
    assert result.startswith("❌ Error en consulta RAG Central:")


def test_query_article_format():
    """Verifica que el output de consulta tenga el formato esperado."""
    class FakeMemoryQuery:
        def __init__(self, *args, **kwargs):
            pass

        def recall(self, query, n_results, collection):
            return [
                {
                    "content": "Artículo 1. El Estado garantiza la planificación.",
                    "metadata": {"source_name": "Constitución"},
                }
            ]

    normative_query.AgentMemory = FakeMemoryQuery

    result = normative_query.query_article("Constitución", n=1)
    assert "FUENTE CENTRAL: Constitución" in result
    assert "Artículo 1. El Estado garantiza la planificación." in result
    assert isinstance(result, str)


def test_query_article_no_results(monkeypatch):
    class EmptyMemoryQuery:
        def __init__(self, *args, **kwargs):
            pass

        def recall(self, query, n_results, collection):
            return []

    monkeypatch.setattr(normative_query, "AgentMemory", EmptyMemoryQuery)

    result = normative_query.query_article("Vacío", n=1)
    assert result == "No se encontró información para: Vacío en la memoria central."


# --- Research Loader Tests ---

def test_ask_brain_uses_recovered_context(monkeypatch):
    class FakeResearchBrain:
        def get_context(self, question, top_n=3):
            return f"contexto:{question}:{top_n}"

        def search(self, topic, top_n=2):
            return [
                {
                    "content": "Fragmento 1",
                    "metadata": {"source_name": "Constitución"},
                },
                {
                    "content": "Fragmento 2",
                    "metadata": {"source_name": "COPFP"},
                },
            ]

    monkeypatch.setattr(research_module, "brain_engine", FakeResearchBrain())

    assert research_module.ask_brain("¿Qué es el SNIP?", depth=4) == "contexto:¿Qué es el SNIP?:4"

    citations = research_module.search_citations("planificación")
    assert citations == ['"Fragmento 1" (Constitución)', '"Fragmento 2" (COPFP)']


def test_search_citations_supports_legacy_chroma_shape(monkeypatch):
    class FakeLegacyBrain:
        def get_context(self, question, top_n=3):
            return "contexto legado"

        def search(self, topic, top_n=2):
            return {
                "documents": [["Texto legado"]],
                "metadatas": [[{"source_name": "Legado"}]],
            }

    monkeypatch.setattr(research_module, "brain_engine", FakeLegacyBrain())

    assert research_module.search_citations("tema") == ['"Texto legado" (Legado)']


# --- Cleanup Guide Utility Tests ---

def test_clean_guide_removes_noise_lines(tmp_path, capsys):
    source = tmp_path / "guide.md"
    source.write_text(
        "Pág. 1 de 10\n"
        "https://edicioneslegales.com.ec/aviso\n"
        "Todos los derechos reservados.\n"
        "Fiel Web Ediciones Legales\n"
        "Gráfico 1. Mapa conceptual 12\n"
        "## Sección principal\n"
        "Art. 1. El contenido se conserva.\n"
        "\f",
        encoding="utf-8",
    )

    clean_guide(source)

    cleaned = source.read_text(encoding="utf-8")
    output = capsys.readouterr().out

    assert "Cleanup complete" in output
    assert "Original lines: 8 | Cleaned lines: 3" in output
    assert "Pág. 1 de 10" not in cleaned
    assert "https://edicioneslegales.com.ec/aviso" not in cleaned
    assert "Gráfico 1. Mapa conceptual 12" not in cleaned
    assert "## Sección principal" in cleaned
    assert "Art. 1. El contenido se conserva." in cleaned
    assert "\f" not in cleaned


def test_clean_guide_missing_file(capsys):
    clean_guide("/tmp/does-not-exist-guide.md")

    output = capsys.readouterr().out
    assert "File not found" in output
