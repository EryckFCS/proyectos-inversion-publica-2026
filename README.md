# Laboratorio de Proyectos de Inversión Pública (LPI)

## Universidad Nacional de Loja | Séptimo Ciclo de Economía

![Build Status](https://img.shields.io/github/actions/workflow/status/EryckFCS/proyectos-inversion-publica-2026/academic_ci.yml?branch=main&label=Build&style=for-the-badge)
![Data Integrity](https://img.shields.io/badge/Integridad%20de%20Datos-Verificada-green?style=for-the-badge)
![Nivel de Investigación](https://img.shields.io/badge/Nivel%20de%20Investigación-5-blueviolet?style=for-the-badge)

## ¿Qué es el LPI?

El **Laboratorio de Proyectos de Inversión Pública (LPI)** es un entorno de trabajo diseñado para que la teoría económica no se quede solo en el papel. Es el espacio donde centralizamos toda la investigación, el análisis normativo y el modelado técnico necesario para entender cómo se gestiona la inversión en el Ecuador.

Este laboratorio ha sido creado para transformar la forma en que abordamos la materia, pasando de una simple entrega de documentos a una gestión profesional del conocimiento económico.

## ¿A qué necesidad responde? 

El manejo de proyectos de inversión pública en el mundo real es complejo, disperso y exige un orden impecable. Los problemas que atacamos con este sistema son:

- **La dispersión de la información**: Es común que la normativa, los datos y los informes terminen regados en mil carpetas. Aquí, todo tiene un lugar lógico y conectado.
- **La falta de trazabilidad**: Muchas veces no sabemos de dónde salió un dato o qué ley sustenta un informe. Aquí, cada dato tiene su "partida de nacimiento" (linaje) y cada conclusión tiene un respaldo normativo verificado.
- **La complejidad normativa**: En el Ecuador, las reglas cambian (COOTAD, COPFP, guías de SENPLADES). El laboratorio centraliza este conocimiento para que no sea un obstáculo, sino una base sólida.

## Objetivos del Laboratorio

Buscamos que la formación en este ciclo sea de alto nivel, con tres metas claras:

1. **Centralizar el Pensamiento Crítico**: Unificar en un solo lugar la normativa nacional con el análisis técnico-científico.
2. **Garantizar la Rigurosidad**: Que cada tabla, gráfico o informe que generemos sea confiable y esté técnicamente bien fundamentado.
3. **Preparación para el Campo Profesional**: Manejar la información con la misma seriedad y estructura que exige el Sistema Nacional de Inversión Pública (SNIP).

## ¿Cómo está organizado?

El laboratorio se divide en áreas claras para que el trabajo fluya sin confusiones:

- **`docs/evidence/`**: El corazón del portafolio. Aquí se documentan las actividades de Diagnóstico, Marco Lógico y Evaluación. Cada intervención tiene su espacio dedicado con sus informes y respaldos.
- **`src/` & `scripts/`**: El motor técnico. Aquí vive la lógica que procesa los datos, los evaluadores automáticos y las herramientas de inteligencia que ayudan a consultar la normativa.
- **`config/`**: El "manual de reglas". Donde definimos los parámetros, metas y fuentes oficiales para que todo el laboratorio hable el mismo idioma.

## Guía Rápida para el Usuario

Para mantener el laboratorio funcionando y generar los reportes actualizados:

```bash
# Para actualizar los reportes del portafolio (Quarto)
uv run quarto render

# Para verificar que la información es íntegra y no hay errores
uv run python scripts/audit_lab.py
```

## Compromisos de Calidad

- **Normas APA 7**: Rigor en el uso de fuentes y citas.
- **Reproducibilidad**: Si algo cambia en los datos o la ley, el laboratorio se actualiza de forma coherente en todo el sistema.
- **Excelencia en Gestión**: Orden, claridad y sustento técnico en cada paso.

---

*LPI - Economía UNL 2026. Investigación con rigor para el desarrollo nacional.*
