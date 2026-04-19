from scripts.normative_query import query_article


def test_query_article_no_store():
    """Verifica que el sistema maneje la ausencia de la base de datos."""
    # Intentar consultar en una ruta inexistente o sin datos
    result = query_article("test query", collection="non_existent_collection")
    assert "Error" in result or "No se encontró" in result


def test_query_article_format():
    """Verifica que el output de consulta tenga el formato esperado."""
    # Presuponemos que la base de datos existe tras el indexado realizado
    result = query_article("Constitución", n=1)
    assert "FUENTE" in result
    assert isinstance(result, str)
