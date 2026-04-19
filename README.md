# Laboratorio de Inversión Pública (LPI) v5.0

![Build Status](https://img.shields.io/github/actions/workflow/status/EryckFCS/proyectos-inversion-publica-2026/academic_ci.yml?branch=main&label=Build&style=for-the-badge)
![Data Integrity](https://img.shields.io/badge/Data%20Integrity-Verified-green?style=for-the-badge&logo=auditfree)
![Research Level](https://img.shields.io/badge/Research%20Level-Level%206%20(Autonomous)-blueviolet?style=for-the-badge)

Infraestructura técnica para el análisis, formulación y evaluación de proyectos de inversión en el séptimo ciclo de la Carrera de Economía (UNL).

## 🚀 Filosofía de Trabajo: Arquitectura v2.0

Este repositorio no es una carpeta de tareas personal; es un **Laboratorio de Investigación** diseñado para ser escalable, reproducible y auditable. 

Utilizamos un sistema de **Bóvedas Atómicas**: cada actividad académica es un módulo independiente que contiene su propio código, datos locales y reportes, evitando el desorden organizacional a largo plazo.

## 📂 Organización del Laboratorio

```text
.
├── docs/
│   ├── evidence/        # Portafolio de evidencias (Sílabo)
│   │   └── U1-Diag.../   # Unidad 1: Bóvedas ACD, APE, AA
│   └── projects/        # Investigación Core (Proyecto Maestro)
├── src/                 # Motor de cálculo del laboratorio
├── data/                # Capas de datos (Raw -> Analytic)
└── writing/             # Recursos globales (APA 7, Plantillas)
```

## 🛠️ Requisitos de Operación

El laboratorio depende de **[uv](https://astral.sh/uv)** para la gestión de entornos y **[Quarto](https://quarto.org/)** para el renderizado de reportes.

### Renderizado de Reportes
Para generar el portafolio completo con navegación lateral:
```bash
uv run quarto render
```

Para renderizar una actividad específica:
```bash
uv run quarto render docs/evidence/UX/.../index.qmd
```

## 📐 Estándares de Calidad
- **Citas**: Formato APA 7mo Manual mediante BibTeX.
- **Visualización**: Gráficos paramétricos en Matplotlib/Seaborn y diagramas Mermaid.
- **Trazabilidad**: Todo resultado en `docs/` debe ser reproducible mediante scripts en `src/`.

---
*LPI - Seventh Cycle Economics. UNL 2026. Excellence in Public Investment Research.*
