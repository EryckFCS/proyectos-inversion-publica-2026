# Arquitectura Técnica del Nodo PIP

Este repositorio opera como nodo puro. La lógica general vive en `ecs_quantitative`; aquí solo se mantienen las fronteras académicas y los wrappers mínimos que necesita la materia.

## Capas reales

- `config/`: `params.yaml` y `data_catalog.yaml`
- `data/raw/marco_normativo/`: corpus normativo auditado
- `docs/evidence/`: evidencia académica. Hoy solo se publica U1
- `src/core/`: `config.py` y `brain.py`
- `src/lib/`: `formulacion.py` y `research.py`
- `src/orchestration/`: `M01-U1-PIP-Master_Build.py`
- `scripts/`: `sync_brain.py`, `normative_indexer.py`, `normative_query.py`, `audit_lab.py`
- `writing/templates/`: bloques Quarto como `audit_block.qmd`

## Contratos

- `src.core.brain.LaboratorioBrain` encapsula `AgentMemory` central.
- `src.lib.research` formatea contexto y citas desde `LaboratorioBrain`.
- `scripts/normative_indexer.py` indexa en el cerebro central; no crea persistencia local.
- `src/orchestration/M01-U1-PIP-Master_Build.py` usa `LineageEngine` de `ecs_quantitative.core.audit`.
- `scripts/audit_lab.py` localiza la librería central por import, no por ruta fija.

## Límites

- No hay wrapper local para `lineage` ni para evaluación financiera.
- La navegación pública no expone U2/U3 hasta que tengan evidencia real.
- El vector store autorizado es `~/.capital/brain/vector_store`.
