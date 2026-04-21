from scripts.cleanup_guide import clean_guide


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
