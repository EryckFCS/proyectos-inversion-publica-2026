import pytest

from src.lib.formulacion import calcular_brecha, proyectar_demanda


def test_proyectar_demanda_compuesta():
    assert proyectar_demanda(100.0, 0.1, 2) == pytest.approx([100.0, 110.0, 121.0])


def test_calcular_brecha_recorta_en_cero():
    assert calcular_brecha([80, 120, 150], 100) == [0, 20, 50]
