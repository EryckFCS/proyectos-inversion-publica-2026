# Laboratorio de Proyectos de Inversión Pública (PIP)

Nodo federado del curso de Proyectos de Inversión Pública. Este repositorio publica la evidencia viva de la Unidad 1 y las utilidades técnicas mínimas que consumen `ecs_quantitative` como librería central.

## Estado real

- Evidencia pública activa: [Unidad 1](docs/vaults/U1-Diagnostico/ACD-01-Marco-Normativo/index.qmd)
- Unidades 2 y 3: scaffold interno, no publicadas en la navegación principal
- Memoria RAG: `~/.capital/brain/vector_store`
- Cálculo y auditoría: delegados a `ecs_quantitative`
- Sin vector store local persistente

## Estructura útil

- `src/core/`: configuración y wrapper del cerebro central
- `src/lib/`: utilidades de formulación e investigación
- `src/orchestration/`: orquestador de salud del nodo
- `scripts/`: sincronización, consulta normativa y auditoría
- `docs/vaults/`: evidencia académica del sílabo
- `docs/writing/`: entrega canónica, bibliografía y capa Quarto activa
- `docs/management/`: roadmap, arquitectura y riesgos
- `writing/`: plantillas históricas mientras termina la migración

## 📄 Arquitectura de Reporteo (Quarto)

La redacción de informes y evidencia académica sigue el **Estándar Nivel 5**:

- El archivo `_quarto.yml` reside en la **raíz del repositorio**.
- Todo el output generado (HTML/PDF intermedios, dependencias JS/CSS) se concentra automáticamente en el directorio `_site/` o `dist/`.
- No existen carpetas `*_files/` ad-hoc. Todo está cubierto por el `.gitignore` canónico.

## Ejecución

```bash
uv sync
uv run pytest
uv run python scripts/audit_lab.py
uv run python src/orchestration/M01-U1-PIP-Master_Build.py
uv run quarto render docs/writing/delivery/index.qmd
```

## Notas

- No existe un proyecto maestro publicado en `docs/projects/`.
- La documentación canónica de lectura está en [docs/README.md](docs/README.md).
