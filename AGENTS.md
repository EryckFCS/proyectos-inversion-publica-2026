# AGENTS.md - Nodo Federado: Proyectos de Inversion Publica

> Este repositorio es un Nodo Puro de la Arquitectura Federada v8.0.0.
> Opera bajo la Constitucion centralizada en `capital-workstation-libs`.

## Constitucion

```text
/home/erick-fcs/Capital_Workstation/capital-workstation-libs/.github/copilot-instructions.md
```

## 1. Identidad del Nodo y Gobernanza

| Campo | Valor |
| --- | --- |
| **Nodo** | Proyectos de Inversion Publica (PIP) |
| **Materia** | Proyectos de Inversion Publica - 7mo Ciclo |
| **Estado** | Activo - Master Blueprint v8.0.0 Migrated |
| **Docente** | Econ. Jose Job Chamba Tandazo |
| **Estudiante** | Erick Fabricio Condoy Seraquive |
| **Libreria Central** | `ecs_quantitative` (capital-workstation-libs) |
| **Nivel de Inteligencia** | 5 - Intelligent Ecosystem with Controlled Autonomy |
| **Gatekeeper** | `tests/system/test_architecture.py` |
| **QA complementaria** | `tests/test_orchestration.py`, `tests/test_formulacion.py` |
| **RAG** | `marco_normativo` en `~/.capital/brain/vector_store/`; `bibliography/` conserva `bibliography_index.json` y `rag_status.json` |

## 2. Capacidades de Inteligencia (v3.0)

Este nodo esta disenado para producir gestion de proyectos reproducible con trazabilidad normativa completa.

1. Normative Project Audit: evaluacion de proyectos contra el marco normativo, metodologias y lineamientos vigentes.
2. Federated Knowledge Consumption: integracion con `ecs_quantitative` para formulacion, evaluacion y seguimiento de proyectos.
3. Atomic Evidence Mapping: trazabilidad absoluta entre lecturas, evidencia de campo y entregables Quarto.
4. Project Formulation Engine: separa la logica de formulacion en `src/lib/formulacion.py` y la capa de investigacion en `src/lib/research.py`.

## 3. Protocolos Operativos

### 3.1. Contractual QA Protocol

- Invariante: ningun cambio se considera estable si rompe el contrato de orquestacion o los contratos de datos del nodo.
- Accion: ejecutar `uv run pytest tests/system/test_architecture.py` antes de cerrar cambios de conducta o estructura.
- Falla: si alguno falla, se corrige la causa raiz antes de continuar.

### 3.2. Research Protocol

- Deteccion: identificar si la tarea toca identificacion, formulacion, evaluacion o seguimiento.
- Ubicacion: la logica de ejecucion vive en `src/core/`, `src/lib/`, `src/tasks/` y `src/orchestration/`; la evidencia reproducible vive en `docs/evidence/`, la narrativa en `docs/writing/`, la gestion en `docs/management/` y el marco normativo en `data/raw/marco_normativo/`.
- Registro: cada analisis debe dejar logs en el vault local correspondiente y mantener sincronizados `bibliography_index.json` y `rag_status.json`.

## 4. Arquitectura de Bovedas (Nivel 5)

### 4.1. Estructura Analitica

```text
.
├── config/                  # Catalogos y parametros del nodo
├── data/                    # Datos del proyecto y marco normativo
├── docs/
│   ├── evidence/            # Workshops, informes y aplicaciones tecnicas
│   ├── writing/             # Narrativa canónica y entrega Quarto
│   ├── management/          # Planning, arquitectura y riesgos
│   ├── readings/            # Lecturas y marco normativo
│   └── syllabus/            # Syllabus oficial e institucional
├── reports/                 # Entregables institucionales finales
├── bibliography/            # raw/, processed/, sanitized/
├── scripts/                 # Utilidades transversales
├── src/                     # Core logic and domain wrappers
└── tests/                   # Gatekeepers and regression checks
```

### 4.2. Capas Documentales

- `docs/evidence/`: unidades como `U1-Diagnostico/` y `U2-Marco-Logico/` con evidencia reproducible.
- `docs/writing/`: narrativa final, bibliografía canónica y unidad de entrega.
- `docs/management/`: planning, arquitectura y riesgos del nodo.
- `docs/readings/`: lecturas tecnicas, marco normativo y material de apoyo.
- `docs/syllabus/`: syllabus oficial y documentos institucionales.
- `bibliography/`: cache canonico de referencias con `raw/`, `processed/` y `sanitized/`.
- `reports/`: entregables institucionales finales (antes `deliveries/`).ales.

## 5. Estrategia de Resiliencia

1. Zero Floating Doctrine: no deben flotar scripts analiticos en la raiz; la logica operativa debe quedarse en `src/` o en los sub-vaults de evidencia.
2. Path Integrity: resolver rutas con `pathlib` y la configuracion del proyecto, no con rutas codificadas a mano.
3. Data Lineage: la curacion y normalizacion deben preservar trazabilidad en logs, catalogos y entregables.
4. Local Module Whitelist: los modulos `src/lib/formulacion.py` y `src/lib/research.py` son locales por diseno y no deben moverse a la libreria central sin una propuesta formal.

## 6. Entorno y Mantenimiento

```bash
uv sync
PYTHONPATH=src .venv/bin/python -m pytest tests/test_orchestration.py tests/test_formulacion.py
uv run python src/orchestration/M01-U1-PIP-Master_Build.py
uv run python scratch/test_central_rag.py
quarto render docs/writing/delivery/index.qmd --to pdf
```

## Regla de Oro

> Si algo que construyas aqui sirve para otras materias, proponlo para la libreria central.
