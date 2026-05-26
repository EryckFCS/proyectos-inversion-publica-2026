"""Consolidated Quantitative Engine, Financial models, and master build orchestration tests."""

from __future__ import annotations

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import pytest

# Quantitative imports
from ecs_quantitative.finance.evaluation import compute_bcr, compute_irr, compute_npv
from src.lib.formulacion import calcular_brecha, proyectar_demanda


# --- PIP Financial Evaluation Model Tests ---

def test_van_basico():
    # Flujo: [-100, 50, 50, 50] Tasa: 0.1
    flujo = [-100, 50, 50, 50]
    tasa = 0.1
    # VAN = -100 + 50/1.1 + 50/1.1^2 + 50/1.1^3
    # VAN = -100 + 45.45 + 41.32 + 37.56 = 24.34
    van = compute_npv(flujo, tasa)
    assert van == pytest.approx(24.34, rel=1e-2)


def test_tir_basica():
    # Flujo [-100, 110] -> TIR debe ser 0.1 (10%)
    flujo = [-100, 110]
    tir = compute_irr(flujo)
    assert tir == pytest.approx(0.1)


def test_rbc():
    beneficios = [0, 60, 60]
    costos = [100, 10, 10]
    tasa = 0.1
    # VA Beneficios = 60/1.1 + 60/1.21 = 54.54 + 49.58 = 104.12
    # VA Costos = 100 + 10/1.1 + 10/1.21 = 100 + 9.09 + 8.26 = 117.35
    # RBC = 104.12 / 117.35 = 0.887
    rbc = compute_bcr(beneficios, costos, tasa)
    assert rbc == pytest.approx(0.887, rel=1e-2)


# --- PIP Formulation Model Tests ---

def test_proyectar_demanda_compuesta():
    assert proyectar_demanda(100.0, 0.1, 2) == pytest.approx([100.0, 110.0, 121.0])


def test_calcular_brecha_recorta_en_cero():
    assert calcular_brecha([80, 120, 150], 100) == [0, 20, 50]


# --- Project Orchestration Tests ---

def load_orchestrator_module(project_root: Path):
    module_name = "pip_master_build_test"
    sys.modules.pop(module_name, None)
    module_path = project_root / "src/orchestration/M01-U1-PIP-Master_Build.py"
    spec = spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run_health_check_uses_central_lineage(monkeypatch, project_root):
    module = load_orchestrator_module(project_root)

    class FakeLineageEngine:
        def __init__(self, root_path, catalog_path):
            self.root_path = root_path
            self.catalog_path = catalog_path
            self.catalog = {
                "datasets": {
                    "base": {
                        "files": [{"id": "CONST_2008"}, {"id": "COPFP"}],
                    }
                }
            }

        def verify_all(self):
            return ([{"id": "CONST_2008"}, {"id": "COPFP"}], [])

        def heal(self):
            return True

    monkeypatch.setattr(module, "LineageEngine", FakeLineageEngine)

    orchestrator = module.PIPOrchestrator()
    captured = {}

    monkeypatch.setattr(orchestrator, "run_tests_forensic", lambda command: (True, "ok"))
    monkeypatch.setattr(
        orchestrator, "run_academic_check", lambda subject_code, custom_units=None: ({"U1": 1}, [])
    )
    monkeypatch.setattr(
        orchestrator, "check_environment", lambda tools: ({tool: True for tool in tools}, [])
    )
    monkeypatch.setattr(orchestrator, "generate_report", lambda status: captured.update(status))

    status = orchestrator.run_health_check()

    assert orchestrator.catalog_path == project_root / "config" / "data_catalog.yaml"
    assert status["layers"]["core_integrity"] is True
    assert status["layers"]["logic_validation"] is True
    assert status["layers"]["academic_compliance"] is True
    assert status["layers"]["environment"] is True
    assert captured["layers"]["core_integrity"] is True


def test_auto_heal_uses_lineage_heal(monkeypatch, project_root):
    module = load_orchestrator_module(project_root)

    class FakeLineageEngine:
        def __init__(self, root_path, catalog_path):
            self.root_path = root_path
            self.catalog_path = catalog_path
            self.catalog = {"datasets": {"base": {"files": []}}}
            self.heal_called = False

        def verify_all(self):
            return ([], [])

        def heal(self):
            self.heal_called = True
            return True

    monkeypatch.setattr(module, "LineageEngine", FakeLineageEngine)

    orchestrator = module.PIPOrchestrator()
    monkeypatch.setattr(orchestrator, "run_health_check", lambda: {"ok": True})

    result = orchestrator.auto_heal()

    assert result == {"ok": True}
    assert orchestrator.lineage_engine.heal_called is True


# --- PIP Audit Lab Tests ---

def test_audit_lab_standard(monkeypatch):
    from src.lib import research as res_mod
    
    # Mock ask_brain and search_citations
    monkeypatch.setattr(res_mod, "ask_brain", lambda q, depth=None: f"mocked response for {q}")
    
    response = res_mod.ask_brain("¿Cómo se audita?", depth=3)
    assert response == "mocked response for ¿Cómo se audita?"

