import pytest
from src.lib.evaluacion import calcular_van, calcular_tir, calcular_rbc

def test_van_basico():
    # Flujo: [-100, 50, 50, 50] Tasa: 0.1
    flujo = [-100, 50, 50, 50]
    tasa = 0.1
    # VAN = -100 + 50/1.1 + 50/1.1^2 + 50/1.1^3
    # VAN = -100 + 45.45 + 41.32 + 37.56 = 24.34
    van = calcular_van(flujo, tasa)
    assert van == pytest.approx(24.34, rel=1e-2)

def test_tir_basica():
    # Flujo [-100, 110] -> TIR debe ser 0.1 (10%)
    flujo = [-100, 110]
    tir = calcular_tir(flujo)
    assert tir == pytest.approx(0.1)

def test_rbc():
    beneficios = [0, 60, 60]
    costos = [100, 10, 10]
    tasa = 0.1
    # VA Beneficios = 60/1.1 + 60/1.21 = 54.54 + 49.58 = 104.12
    # VA Costos = 100 + 10/1.1 + 10/1.21 = 100 + 9.09 + 8.26 = 117.35
    # RBC = 104.12 / 117.35 = 0.887
    rbc = calcular_rbc(beneficios, costos, tasa)
    assert rbc == pytest.approx(0.887, rel=1e-2)
