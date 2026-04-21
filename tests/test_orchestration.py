import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


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
