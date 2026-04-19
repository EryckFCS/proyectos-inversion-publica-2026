# Arquitectura Técnica: LPI - Laboratorio de Proyectos de Inversión

Este documento define la infraestructura técnica para la materia de **Proyectos de Inversión Pública (PIP)**, basada en los estándares del CIE.

## 🏛️ Capas del Sistema

### 1. Núcleo (Core) (`src/core/`)
Implementa las invariantes del marco de inversión pública:
- **`config.py`**: Gestión dinámica de rutas y perfiles de proyecto.
- **`precios_sociales.py`**: Repositorio de factores de corrección (mano de obra, divisas, tasa social de descuento) oficiales de SENPLADES o entidades reguladoras.
- **`utils.py`**: Funciones auxiliares para normalización de datos territoriales.

### 2. Motor de Evaluación (Library) (`src/lib/`)
Lógica de cálculo agnóstica al proyecto específico:
- **`formulacion.py`**: Algoritmos para proyección de demanda, balance oferta-demanda y determinación de brechas.
- **`evaluacion.py`**: Cálculo matricial de indicadores financieros y sociales (VAN, TIR, RBC, VAC).
- **`data_doctor.py`**: Validador de consistencia en flujos de caja y metadatos de proyectos.

### 3. Zona de Datos (`data/`)
Organización para auditoría académica:
- **`raw/`**: Datos de diagnósticos, censos o estudios de campo sin procesar.
- **`curation/`**: Salida de scripts de limpieza y normalización.
- **`analytic/`**: Matrices de flujos de caja y resultados finales de evaluación.

### 4. Orquestación y Tareas (`src/tasks/` y `src/orchestration/`)
Scripts de ejecución siguiendo el sílabo:
- **`Txx-Ux-PIP-[Tema].py`**: Scripts individuales por unidad de aprendizaje.
- **`Mxx-Ux-PIP-Master_Build.py`**: Orquestadores de unidad para entregas finales.

---

## 📐 Doctrina de Modelado

1.  **Separación de Flujos**: El flujo de caja financiero y el flujo social deben mantenerse desacoplados mediante capas de corrección.
2.  **Transparencia de Parámetros**: Prohibido el uso de "Magic Numbers". Todas las tasas y parámetros deben provenir de `src/core/precios_sociales.py`.
3.  **Auditoría Forense**: Todo cálculo debe ser trazable hasta la fuente original de los datos en `data/raw/`.

---

## 🛠️ Entorno de Desarrollo

El sistema está optimizado para su ejecución con `uv`.
```bash
uv pip install -e .
```

---
*LPI - Estándar v1.0. 2026.*
