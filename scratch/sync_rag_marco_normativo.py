"""
sync_rag_marco_normativo.py
Script de ingesta idempotente para el lóbulo `marco_normativo` (PIP).
Fuente: docs/readings/ — PDFs de marcos normativos de inversión pública.
NOTA: Los 1,162 chunks actuales son de 'agent_memory', no de los PDFs.
      Este script indexa los PDFs reales del nodo.
"""
import json
from pathlib import Path
from ecs_quantitative.ingestion.rag import BibliographyRAG, CorpusEntry
from loguru import logger

BASE_PATH = Path(__file__).parent.parent
STATUS_FILE = BASE_PATH / "bibliography" / "rag_status.json"

FILES_TO_INGEST = [
    {
        "id": "pip_aspectos_generales",
        "name": "Aspectos Generales — Proyectos de Inversión Pública",
        "path": str(BASE_PATH / "docs" / "readings" / "ASPECTOS GENERALES PROYECTOS DE INVERSIÓN.pdf"),
    },
    {
        "id": "pip_actividad_contacto_1",
        "name": "Actividad de Contacto Docente 1 — PIP",
        "path": str(BASE_PATH / "docs" / "readings" / "Actividad_Contacto_Docente_1-signed.pdf"),
    },
]


def sync():
    rag = BibliographyRAG(
        collection_name="marco_normativo",
        ocr_enabled=False,
        formula_enabled=False,
    )

    logger.info(f"Iniciando ingesta en lóbulo 'marco_normativo' — {len(FILES_TO_INGEST)} archivos PDF reales")
    total_chunks = 0

    for f in FILES_TO_INGEST:
        entry = CorpusEntry(**f)
        p = Path(entry.path)
        if not p.exists():
            logger.error(f"Archivo no encontrado: {entry.path}")
            continue

        logger.info(f"Procesando: {entry.name} ({p.stat().st_size / 1024 / 1024:.1f} MB)")
        stats = rag.index_entry(entry, include_text=True, include_formulas=False)
        chunks = stats.get("text_chunks", 0)
        total_chunks += chunks
        logger.success(f"✓ {entry.name}: {chunks} fragmentos indexados")

    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    status = {
        "status": "synchronized",
        "last_sync": __import__("datetime").date.today().isoformat(),
        "engine": "ecs_quantitative.ingestion.rag",
        "method": "text-only",
        "target_lobule": "marco_normativo",
        "total_files": len(FILES_TO_INGEST),
        "total_chunks_added": total_chunks,
        "scope": "docs/readings/ — PDFs normativos reales",
        "note": (
            "ADVERTENCIA: Los 1162 chunks previos son de 'agent_memory' (sesiones pasadas). "
            "Este script añade los PDFs reales del nodo. Para purgar agent_memory, se requiere acción separada."
        ),
    }
    STATUS_FILE.write_text(json.dumps(status, ensure_ascii=False, indent=2))
    logger.success(f"Ingesta completa. Total nuevos chunks: {total_chunks}")


if __name__ == "__main__":
    sync()
