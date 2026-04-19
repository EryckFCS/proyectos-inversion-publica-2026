from src.core.brain import brain_engine


def ask_brain(question, depth=3):
    """
    Función de conveniencia para que el estudiante consulte al cerebro
    desde sus reportes Quarto.
    """
    return brain_engine.get_context(question, top_n=depth)


def search_citations(topic):
    """
    Busca citas textuales relevantes para un tema.
    """
    results = brain_engine.search(topic, top_n=2)
    citations = []

    if isinstance(results, dict) and "documents" in results and results["documents"]:
        for i, text in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            source = meta.get("source_name", "Fuente")
            citations.append(f'"{text}" ({source})')

    return citations
