from scripts import normative_query


def test_query_article_no_store():
    """Verifica que el sistema maneje la ausencia de la base de datos."""

    class FailingMemory:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("memoria no disponible")

    normative_query.AgentMemory = FailingMemory

    result = normative_query.query_article("test query", collection="non_existent_collection")
    assert result.startswith("❌ Error en consulta RAG Central:")


def test_query_article_format():
    """Verifica que el output de consulta tenga el formato esperado."""

    class FakeMemory:
        def __init__(self, *args, **kwargs):
            pass

        def recall(self, query, n_results, collection):
            return [
                {
                    "content": "Artículo 1. El Estado garantiza la planificación.",
                    "metadata": {"source_name": "Constitución"},
                }
            ]

    normative_query.AgentMemory = FakeMemory

    result = normative_query.query_article("Constitución", n=1)
    assert "FUENTE CENTRAL: Constitución" in result
    assert "Artículo 1. El Estado garantiza la planificación." in result
    assert isinstance(result, str)


def test_query_article_no_results(monkeypatch):
    class EmptyMemory:
        def __init__(self, *args, **kwargs):
            pass

        def recall(self, query, n_results, collection):
            return []

    monkeypatch.setattr(normative_query, "AgentMemory", EmptyMemory)

    result = normative_query.query_article("Vacío", n=1)
    assert result == "No se encontró información para: Vacío en la memoria central."
