# Arquitectura Técnica: LPI - Laboratorio de Proyectos de Inversión

Este documento define la infraestructura técnica para la materia de **Proyectos de Inversión Pública (PIP)**, basada en los estándares del CIE.

## 🏛️ Estructura de Directorios

El repositorio se organiza siguiendo una lógica de ingeniería de datos y reporte académico:

### Gestión y Configuración
- **`config/`**: Archivos de configuración (.yaml, .json) para parámetros globales del sistema.
- **`src/`**: Código fuente principal (Core, Lib, Tasks).
- **`scripts/`**: Utilidades para automatización, despliegue y migración de datos.
- **`tests/`**: Suite de pruebas unitarias e integración para validar la lógica de cálculo.

### Zona de Datos
- **`data/`**: Organización para auditoría académica.
    - `raw/`: Datos originales sin procesar.
    - `curation/`: Datos limpios y normalizados.
    - `analytic/`: Resultados finales y matrices de flujos.

### Reportes e Investigación (docs/)
- **`docs/evidence/`**: Portafolio de evidencias académicas (Syllabus).
    - `UX-Nombre/`: Carpeta por unidad.
    - `ACD-XX/`: Bóveda atómica por actividad (index.qmd + assets).
- **`docs/projects/`**: Investigación central y proyectos de largo plazo.
- **`writing/`**: Recursos de redacción global (APA 7, CSL, plantillas LaTeX).
- **`deliveries/`**: Repositorio de versiones finales firmadas y publicadas.

### Operación Local (Excluidos de Git)
- **`logs/`**: Registros detallados de ejecución del sistema para depuración técnica.
- **`scratch/`**: Espacio de trabajo volátil para guiones de prueba y borradores rápidos.

---

## 🏛️ Capas del Sistema (src/)

### 1. Núcleo (Core) (`src/core/`)
Implementa las invariantes del marco de inversión pública:
- **`config.py`**: Gestión dinámica de rutas y perfiles de proyecto.
- **`precios_sociales.py`**: Factores de corrección oficiales (mano de obra, divisas, tasa social).
- **`utils.py`**: Funciones auxiliares para normalización de datos.

### 2. Motor de Evaluación (Library) (`src/lib/`)
- **`formulacion.py`**: Proyecciones de demanda y brechas.
- **`evaluacion.py`**: Indicadores financieros y sociales (VAN, TIR, RBC).
- **`data_doctor.py`**: Validador de consistencia de flujos y metadatos.

---

## 📐 Doctrina de Modelado

1.  **Separación de Flujos**: El flujo de caja financiero y el flujo social deben mantenerse desacoplados.
2.  **Transparencia de Parámetros**: Prohibido el uso de "Magic Numbers".
3.  **Auditoría Forense**: Todo cálculo debe ser trazable hasta la fuente en `data/raw/`.

---

## 🛠️ Entorno de Desarrollo

El sistema está optimizado para su ejecución con `uv`.
```bash
uv run quarto render docs/
```

---
*LPI - Estándar v2.0 (Reseach-Driven Architecture). 2026. Estructura Completa Verificada.*
