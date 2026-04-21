from src.core import brain as brain_module


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
