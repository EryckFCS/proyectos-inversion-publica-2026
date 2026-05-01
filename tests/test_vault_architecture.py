from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"

EVIDENCE_UNITS = [
    DOCS_DIR / "evidence" / "U1-Diagnostico" / "ACD-01-Marco-Normativo",
    DOCS_DIR / "evidence" / "U1-Aspectos-Generales" / "Boveda_Estudio",
    DOCS_DIR / "evidence" / "U2-Marco-Logico",
    DOCS_DIR / "evidence" / "U3-Seguimiento-Evaluacion",
]

CANONICAL_UNITS = [
    DOCS_DIR / "writing" / "delivery",
    DOCS_DIR / "management" / "planning",
]


def _assert_clean_unit(unit_path: Path) -> None:
    assert (unit_path / "index.qmd").is_file(), f"La unidad {unit_path.name} no tiene index.qmd"
    assert (unit_path / "assets").is_dir(), f"La unidad {unit_path.name} no tiene carpeta assets/"

    floating_files = [
        item.name for item in unit_path.iterdir() if item.is_file() and item.name != "index.qmd"
    ]
    assert not floating_files, (
        f"Archivos flotantes prohibidos en {unit_path.name}: {floating_files}"
    )


def test_canonical_vault_roots_exist() -> None:
    for vault_name in ["evidence", "writing", "management", "readings"]:
        assert (DOCS_DIR / vault_name).is_dir(), f"Falta la bóveda docs/{vault_name}/"


def test_writing_support_files_exist() -> None:
    assert (DOCS_DIR / "writing" / "index.qmd").is_file()
    assert (DOCS_DIR / "writing" / "references.bib").is_file()
    assert (DOCS_DIR / "writing" / "apa.csl").is_file()
    assert (DOCS_DIR / "management" / "index.qmd").is_file()


@pytest.mark.parametrize("unit_path", EVIDENCE_UNITS + CANONICAL_UNITS)
def test_unit_structure(unit_path: Path) -> None:
    _assert_clean_unit(unit_path)


def test_acd_assets_and_citations_are_canonical() -> None:
    acd_index = (EVIDENCE_UNITS[0] / "index.qmd").read_text(encoding="utf-8")
    assert "../../../writing/references.bib" in acd_index
    assert "../../../writing/apa.csl" in acd_index
    assert (EVIDENCE_UNITS[0] / "assets" / "Actividad_Contacto_Docente_1-signed.pdf").is_file()
    assert (EVIDENCE_UNITS[0] / "assets" / "mapa-impacto-multidimensional.png").is_file()


def test_boveda_estudio_uses_canonical_writing_vault() -> None:
    boveda_index = (EVIDENCE_UNITS[1] / "index.qmd").read_text(encoding="utf-8")
    assert "../../../writing/references.bib" in boveda_index
    assert "../../../writing/apa.csl" in boveda_index
