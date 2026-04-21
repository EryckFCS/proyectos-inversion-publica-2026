from pathlib import Path

import ecs_quantitative

from scripts import audit_lab


def test_run_central_audit_uses_resolved_core_path(monkeypatch, capsys):
    calls = {}

    class FakeAuditEngine:
        def __init__(self, core_dir):
            calls["core_dir"] = core_dir

        def audit_project(self, project_root):
            calls["project_root"] = project_root
            return {
                "files": 1,
                "loc": 2,
                "lifecycle": "ok",
                "redundancies": [],
                "hardcoded_paths": [],
            }

    monkeypatch.setattr(audit_lab, "AuditEngine", FakeAuditEngine)

    audit_lab.run_central_audit()
    output = capsys.readouterr().out

    assert "Auditoría de Gobernanza Federada" in output
    assert calls["core_dir"] == Path(ecs_quantitative.__file__).resolve().parent
    assert calls["project_root"] == Path(audit_lab.PROJECT_ROOT)
