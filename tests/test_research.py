from src.lib import research as research_module


def test_ask_brain_uses_recovered_context(monkeypatch):
    class FakeBrain:
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

    monkeypatch.setattr(research_module, "brain_engine", FakeBrain())

    assert research_module.ask_brain("¿Qué es el SNIP?", depth=4) == "contexto:¿Qué es el SNIP?:4"

    citations = research_module.search_citations("planificación")
    assert citations == ['"Fragmento 1" (Constitución)', '"Fragmento 2" (COPFP)']


def test_search_citations_supports_legacy_chroma_shape(monkeypatch):
    class FakeBrain:
        def get_context(self, question, top_n=3):
            return "contexto legado"

        def search(self, topic, top_n=2):
            return {
                "documents": [["Texto legado"]],
                "metadatas": [[{"source_name": "Legado"}]],
            }

    monkeypatch.setattr(research_module, "brain_engine", FakeBrain())

    assert research_module.search_citations("tema") == ['"Texto legado" (Legado)']
