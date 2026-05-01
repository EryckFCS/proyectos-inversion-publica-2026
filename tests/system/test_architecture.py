from pathlib import Path
import pytest

def test_evidence_structure():
    """Valida que las bóvedas de evidencia existan en el lugar correcto."""
    root = Path(".")
    vaults_dir = root / "docs" / "vaults"
    legacy_vaults = root / "docs" / "vaults"
    
    assert vaults_dir.exists(), "El directorio docs/evidence/ no existe."
    assert not legacy_vaults.exists(), "El directorio legado docs/vaults/ todavía existe."

def test_zero_floating_doctrine():
    """Valida que no existan directorios prohibidos en la raíz."""
    root = Path(".")
    forbidden = ["writing", "logs", "notebooks", "deliveries", "vaults"]
    
    for folder in forbidden:
        path = root / folder
        assert not path.exists(), f"El directorio '{folder}' no debe estar en la raíz."

def test_bibliography_consolidation():
    """Valida que el pipeline bibliográfico esté consolidado."""
    root = Path(".")
    bib_dir = root / "bibliography"
    markdown_dir = bib_dir / "markdown"
    
    assert bib_dir.exists(), "El directorio bibliography/ no existe."
    assert not markdown_dir.exists(), "El directorio intermedio bibliography/markdown/ todavía existe."

def test_reports_directory():
    """Valida que los entregables estén en reports/."""
    root = Path(".")
    reports_dir = root / "reports"
    legacy_deliveries = root / "deliveries"
    
    assert reports_dir.exists(), "El directorio reports/ no existe."
    assert not legacy_deliveries.exists(), "El directorio legado deliveries/ todavía existe."
