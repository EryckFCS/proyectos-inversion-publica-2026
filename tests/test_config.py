from src.core.config import LPIConfig


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
