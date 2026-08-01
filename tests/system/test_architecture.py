import re
from pathlib import Path
import sys
import pytest

# Localización de la raíz del repositorio relativa a este archivo (tests/system/test_architecture.py)
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))



def test_root_structure():
    """Valida la estructura de directorios Blueprint v8.1.5."""
    required_dirs = [
        "config",
        "data",
        "docs/vaults",
        "docs/management",
        "docs/readings",
        "docs/syllabus",
        "reports",
        "scratch",
        "scripts",
        "src",
        "tests/system",
    ]

    for d in required_dirs:
        assert (REPO_ROOT / d).is_dir(), f"Directorio requerido ausente: {d}"


def test_bibliography_presence():
    """Valida que el directorio de bibliografía exista."""
    bib_dir = REPO_ROOT / "bibliography"
    assert bib_dir.is_dir(), "Directorio 'bibliography/' ausente."
    # Los subdirectorios (processed, markdown, sanitized) son opcionales
    # debido a la centralización en el Data Lake.


def test_zero_floating_doctrine():
    """Enfuerza la Doctrina Zero Floating en la raíz."""
    forbidden_ext = [".ipynb", ".csv", ".xlsx", ".pdf", ".do", ".dta"]
    forbidden_dirs = ["writing", "deliveries", "notebooks", "vaults_legacy"]

    for item in REPO_ROOT.iterdir():
        if item.is_file() and item.suffix in forbidden_ext:
            # Excepción para archivos de configuración o README
            if item.name not in ["README.md", "main.py"]:
                pytest.fail(
                    f"Archivo flotante detectado en raíz: {item.name}. Muévelo a una bóveda."
                )

        if item.is_dir() and item.name in forbidden_dirs:
            pytest.fail(f"Carpeta legada/prohibida detectada en raíz: {item.name}.")


def test_evidence_naming_convention():
    """Valida la convención de nombres de bóvedas de evidencia [unit]-[cat]-[seq]-[slug]."""
    vaults_path = REPO_ROOT / "docs" / "vaults"
    if not vaults_path.exists():
        pytest.skip("No se encontró la carpeta de evidencias.")

    # Patrón estándar: u[X]-[categoría]-[secuencia]-[slug]
    # Patrón especial: [slug] (letras minúsculas y guiones)
    standard_pattern = re.compile(r"^u\d-(aa|ape|acd)-\d{2}-[\w-]+$")
    special_pattern = re.compile(r"^[a-z][a-z0-9-_]+$")

    for item in vaults_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            assert item.name == item.name.lower(), (
                f"La bóveda '{item.name}' debe estar en minúsculas."
            )
            is_valid = standard_pattern.match(item.name) or special_pattern.match(item.name)
            assert is_valid, (
                f"La bóveda '{item.name}' no sigue ninguna convención válida ([unit]-[cat]-[seq]-[slug] o slug simple)."
            )


def test_zero_floating_in_vault_units():
    """Enfuerza la Doctrina Zero Floating dentro de la raíz de cada sub-bóveda y sus sub-unidades."""
    vaults_path = REPO_ROOT / "docs" / "vaults"
    if not vaults_path.exists():
        pytest.skip("No docs/vaults directory found.")

    forbidden_ext = [".docx", ".xlsx", ".pdf", ".csv", ".dta", ".do", ".zip", ".rar"]
    allowed_names = ["index.qmd", "references.bib", "knowledge_map.json", "settings.json", "settings.toml", ".gitignore", "_quarto.yml", "readme.md", "README.md"]

    for p in vaults_path.rglob("*"):
        if p.is_file() and not p.name.startswith("."):
            parts = p.parts
            fine_dirs = {
                "assets", "data", "scripts", "logs", "readings", "scratch", "notebooks", ".quarto", "chapters", "reports",
                "evidencia", "levantamiento_de_informacion"
            }
            if not any(fd in parts for fd in fine_dirs):
                is_forbidden = p.suffix in forbidden_ext or (p.suffix in [".md", ".py"] and p.name not in allowed_names)
                if is_forbidden and "template" not in p.name.lower():
                    pytest.fail(
                        f"Archivo flotante prohibido detectado en la raíz de la bóveda '{p.parent.name}': {p.name}. "
                        f"Por favor muévelo a assets/, data/, scripts/, o readings/."
                    )


def test_governance_files():
    """Valida la presencia de archivos críticos de gobernanza."""
    required_files = ["AGENTS.md", "pyproject.toml", "uv.lock"]
    for f in required_files:
        assert (REPO_ROOT / f).is_file(), f"Archivo de gobernanza ausente: {f}"


def test_bibliography_validation():
    """Valida la integridad de los DOIs y metadatos en el .bib del repositorio usando la librería central."""
    from ecs_quantitative.audit.bibliography import BibliographyValidator
    
    # Buscar el archivo .bib de forma adaptativa
    bib_path = REPO_ROOT / "bibliography" / "references.bib"
    if not bib_path.exists():
        bib_path = REPO_ROOT / "docs" / "writing" / "references.bib"
    if not bib_path.exists():
        pytest.skip("No se encontró ningún archivo de referencias .bib")
        
    validator = BibliographyValidator(timeout=4)
    results = validator.validate_file(bib_path)
    
    mismatch_keys = []
    for res in results:
        if not res["valid"] and res["status"] in ("ERROR_MISMATCH", "ERROR_NOT_FOUND"):
            # Solo fallar si el mismatch es en el campo 'title' (error crítico de DOI) o si no se encuentra el DOI
            if res["status"] == "ERROR_NOT_FOUND":
                mismatch_keys.append((res["key"], res["details"]))
            else:
                critical_mismatches = [m for m in res["mismatches"] if m["field"] == "title"]
                if critical_mismatches:
                    mismatch_keys.append((res["key"], res["details"]))
                else:
                    print(f"Warning: Mismatch menor de publisher para {res['key']}: {res['details']}")
            
    assert not mismatch_keys, f"Se detectaron DOIs incorrectos (mismatch de título): {mismatch_keys}"




