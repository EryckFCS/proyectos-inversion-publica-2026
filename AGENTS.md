# AGENTS.md — Nodo Federado: Proyectos de Inversión Pública

> Este repositorio es un **Nodo Puro** de la Arquitectura Federada v7.4.0.  
> Opera bajo la Constitución centralizada en `capital-workstation-libs`.

---

## Constitución

La Constitución institucional vive en la librería central.  
Consumirla antes de cualquier acción:

```bash
/home/erick-fcs/Capital_Workstation/capital-workstation-libs/.github/copilot-instructions.md
```

---

## Identidad del Nodo

| Campo | Valor |
| :--- | :--- |
| **Nodo** | Proyectos de Inversión Pública (PIP) |
| **Materia** | Proyectos de Inversión Pública — 7mo Ciclo |
| **Docente** | Econ. Jose Job Chamba Tandazo |
| **Estudiante** | Erick Fabricio Condoy Seraquive |
| **Librería Central** | `ecs_quantitative` (capital-workstation-libs) |
| **Tipo** | Nodo Puro — consumidor, no reimplementa lógica |
| **RAG** | `marco_normativo` en `~/.capital/brain/vector_store/` |
| **Período** | Marzo - Agosto 2026 |
| **Estructura** | U1 pública; U2/U3 internas en progreso |

---

## Ley de Nodo Puro (Obligatoria)

1. **No reimplementar** lógica que ya exista en `ecs_quantitative`.
2. **Importar siempre** desde la librería central, sin wrappers locales para lógica central.
3. **Antes de crear** un módulo nuevo, correr `AuditEngine` para detectar si ya existe.
4. **RAG**: nunca crear vector stores locales; usar `~/.capital/brain/vector_store/`.

---

## Entorno

```bash
# Activar entorno
uv sync

# Ejecutar el orquestador maestro
uv run python src/orchestration/M01-U1-PIP-Master_Build.py

# Consulta al cerebro central
uv run python scratch/test_central_rag.py
```

---

## Módulos Permitidos (Locales)

Estos archivos son específicos del dominio de PIP y **no deben moverse** a la librería central:

| Archivo | Razón de existencia |
| :--- | :--- |
| `src/lib/formulacion.py` | Proyección de demanda específica PIP |
| `src/lib/research.py` | Wrapper de `AgentMemory` para el dominio |
| `writing/` | Discurso académico propio de la materia |
| `data/` | Datos del proyecto (nunca en repo Git) |

---

## Skills Activos

Disponibles vía la Constitución central en `.github/skills/`:

- `rag_ops` → para ingestión y consulta del cerebro central
- `validaciondependenciastest` → para validación de entorno y dependencias
- `agent_cognition` → para disciplina operativa del agente

---

## Regla de Oro

> Si algo que necesitas **ya existe** en `ecs_quantitative`, **úsalo**.  
> Si algo que implementaste **sirve en otras materias**, **propónlo para la librería**.  
> El conocimiento acumulado en este nodo pertenece a la federación.
