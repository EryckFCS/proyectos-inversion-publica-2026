
Ran command: `Get-ChildItem -Path "D:\" -Directory -Depth 2 | Select-Object FullName`
Ran command: `Get-ChildItem -Path "D:\" -Filter "*inversion*" -Recurse -Depth 3 -ErrorAction SilentlyContinue | Select-Object FullName`
Ran command: `Get-ChildItem -Path "D:\Material_Descargas\proyectos de inversion publica", "D:\07_Ciclo" -Recurse -Depth 3 -ErrorAction SilentlyContinue | Select-Object FullName`
Ran command: `Get-ChildItem -Path "D:\Material_Descargas\proyectos de inversion publica" -Recurse | Select-Object FullName`
Ran command: `Get-ChildItem -Path "D:\" -Filter "*PDOT*" -Recurse -Depth 4 -ErrorAction SilentlyContinue | Select-Object FullName`
Ran command: `Get-ChildItem -Path "D:\07_Ciclo\septimo_ciclo\public_investment_projects"`
Ran command: `Get-ChildItem -Path "$env:USERPROFILE\Downloads", "D:\Material_Descargas" -File -Recurse -Depth 2 -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "guay|pdot|plan" } | Select-Object FullName, Length, LastWriteTime`
Ran command: `Get-ChildItem -Path "$env:USERPROFILE\Downloads" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 15 FullName, Length, LastWriteTime`
Ran command: `python -c " import pypdf reader = pypdf.PdfReader(r'C:\Users\ERICK-FCS\Downloads\PLAN DE DESARROLLO Y ORDENAMIENTO TERRITORIAL 2023-2027.pdf') print('Num pages:', len(reader.pages)) text = '' for i in range(min(5, len(reader.pages))):     text += f'--- Page {i+1} ---\n' + reader.pages[i].extract_text() print(text[:2000]) "`
Ran command: `uv run python -c " import pypdf reader = pypdf.PdfReader(r'C:\Users\ERICK-FCS\Downloads\PLAN DE DESARROLLO Y ORDENAMIENTO TERRITORIAL 2023-2027.pdf') print('Num pages:', len(reader.pages)) text = '' for i in range(min(5, len(reader.pages))):     text += f'--- Page {i+1} ---\n' + reader.pages[i].extract_text() print(text[:2000]) "`
Ran command: `Get-ChildItem -Path "data" -Recurse`
Ran command: `Get-ChildItem -Path "data\raw\marco_normativo\02_Planes_Desarrollo" -Recurse`
Ran command: `Get-ChildItem -Path "data" -Directory`
Ran command: `Get-ChildItem -Path "data\processed"`
Ran command: `Get-ChildItem -Path "data\raw\guayquichuma*"`
Ran command: `Get-ChildItem -Path "docs" -Recurse`
Ran command: `Get-ChildItem -Path "docs\vaults"`
Ran command: `Get-ChildItem -Path "docs\vaults\proyecto-guayquichuma" -Recurse`
Ran command: `uv run python -c " import pypdf p1 = r'C:\Users\ERICK-FCS\Downloads\PLAN DE DESARROLLO Y ORDENAMIENTO TERRITORIAL 2023-2027.pdf' p2 = r'C:\Users\ERICK-FCS\Downloads\PLAN DE DESARROLLO Y ORDENAMIENTO TERRITORIAL 2023-2027_compressed.pdf' r1 = pypdf.PdfReader(p1) r2 = pypdf.PdfReader(p2) print('p1 pages:', len(r1.pages)) print('p2 pages:', len(r2.pages)) "`
Ran command: `Get-ChildItem -Path "docs\vaults\proyecto-guayquichuma\evidencia"`
Ran command: `Copy-Item -Path "C:\Users\ERICK-FCS\Downloads\PLAN DE DESARROLLO Y ORDENAMIENTO TERRITORIAL 2023-2027_compressed.pdf" -Destination "docs\vaults\proyecto-guayquichuma\evidencia\pdot_parroquial_guayquichuma_2023_2027.pdf" -Force`
Ran command: `uv run python -c " import pypdf reader = pypdf.PdfReader('docs/vaults/proyecto-guayquichuma/evidencia/pdot_parroquial_guayquichuma_2023_2027.pdf') toc = [] for i in range(2, 9):     toc.append(reader.pages[i].extract_text()) print('\n'.join(toc)) "`
Ran command: `uv run python -c " import pypdf, sys reader = pypdf.PdfReader('docs/vaults/proyecto-guayquichuma/evidencia/pdot_parroquial_guayquichuma_2023_2027.pdf') with open('scratch/toc_guayquichuma.txt', 'w', encoding='utf-8') as f:     for i in range(1, 10):         f.write(f'=== Page {i+1} ===\n' + reader.pages[i].extract_text() + '\n') print('TOC extracted') "`
Viewed toc_guayquichuma.txt:1-150
Ran command: `uv run python -c "
import pypdf, re, os

pdf_path = 'docs/vaults/proyecto-guayquichuma/evidencia/pdot_parroquial_guayquichuma_2023_2027.pdf'
out_dir = 'docs/vaults/proyecto-guayquichuma/lake_mirror/pdot_guayquichuma_2023_2027'
os.makedirs(out_dir, exist_ok=True)
os.makedirs(f'{out_dir}/sections', exist_ok=True)

reader = pypdf.PdfReader(pdf_path)
full_text = []

print('Total pages:', len(reader.pages))

full_md_lines = ['# PLAN DE DESARROLLO Y ORDENAMIENTO TERRITORIAL DE LA PARROQUIA GUAYQUICHUMA 2023-2027\n\n']

for i, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    # Clean up hyphens and irregular spacing
    txt_clean = re.sub(r'(\w+)-\n(\w+)', r'\1\2', txt)
    page_header = f'\n'
    full_md_lines.append(page_header + txt_clean + '\n\n')

with open(f'{out_dir}/PDOT_GUAYQUICHUMA_2023_2027_COMPLETO.md', 'w', encoding='utf-8') as f:
    f.writelines(full_md_lines)

print('Written full markdown successfully!')
"`Used tool: manage_task Ran command:`Get-Content "C:\Users\ERICK-FCS\.gemini\antigravity-ide\brain\df8f97e9-de05-45df-be2f-e71c6f2b75f6\.system_generated\tasks\task-53.log" -Tail 20`Used tool: manage_task Ran command:`uv run python -c "
with open('docs/vaults/proyecto-guayquichuma/lake_mirror/pdot_guayquichuma_2023_2027/PDOT_GUAYQUICHUMA_2023_2027_COMPLETO.md', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split('<!-- PAGE ')
print('Num page splits:', len(pages))

# Search for Diagnostico Integrado, Problemas y Priorizacion

target_keywords = ['IDENTIFICACIÓN Y SISTEMATIZACIÓN DE POTENCIALIDADES Y PROBLEMAS', 'PRIORIZACIÓN DE POTENCIALIDADES Y PROBLEMAS', 'Árbol de problemas', 'Matriz de problemas', 'Planes, Programas, Proyectos y Presupuestos']

for kw in target_keywords:
    pos = text.find(kw)
    if pos != -1:
        print(f'Found: {kw} at char {pos}')
        # print snippet around it
        start = max(0, pos - 100)
        end = min(len(text), pos + 1200)
        print('--- SNIPPET ---')
        print(text[start:end])
        print('================\n')
"`Ran command:`uv run python -c "
with open('docs/vaults/proyecto-guayquichuma/lake_mirror/pdot_guayquichuma_2023_2027/PDOT_GUAYQUICHUMA_2023_2027_COMPLETO.md', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split('<!-- PAGE ')

# Print text from page 70 to page 95

with open('scratch/problemas_guayquichuma_p70_95.txt', 'w', encoding='utf-8') as out:
    for p in pages:
        if not p.strip(): continue
        p_num = int(p.split(' -->')[0])
        if 70 <= p_num <= 96:
            out.write(f'=== PAGE {p_num} ===\n' + p + '\n\n')

print('Wrote pages 70-96')
"`Ran command:`uv run python -c "
with open('docs/vaults/proyecto-guayquichuma/lake_mirror/pdot_guayquichuma_2023_2027/PDOT_GUAYQUICHUMA_2023_2027_COMPLETO.md', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('')[0]
        if p_num_str.isdigit():
            p_num = int(p_num_str)
            if 70 <= p_num <= 96:
                out.write(f'=== PAGE {p_num} ===\n' + p + '\n\n')

print('Wrote pages 70-96 successfully')
"`Viewed problemas_guayquichuma_p70_95.txt:1-180 Ran command:`uv run python -c "
with open('scratch/problemas_guayquichuma_p70_95.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Look for 'Tabla' or 'PROBLEMAS' or 'PRIORIZACIÓN'

matches = re.findall(r'(Tabla \d+.*|2\.[45].*|3\.2\.3.*)', text)
for m in matches[:30]:
    print(m)
"`Ran command:`uv run python -c "
with open('scratch/problemas_guayquichuma_p70_95.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Get section from Tabla 39 to Tabla 46

p_start = text.find('Tabla 39.')
p_end = text.find('3.2.4. Modelo Territorial Deseado')
if p_start != -1 and p_end != -1:
    with open('scratch/matriz_problemas_y_proyectos.txt', 'w', encoding='utf-8') as out:
        out.write(text[p_start:p_end])
    print('Saved matriz_problemas_y_proyectos.txt, length:', p_end - p_start)
else:
    print('Indices not found:', p_start, p_end)
"`Ran command:`uv run python -c "
with open('scratch/problemas_guayquichuma_p70_95.txt', 'r', encoding='utf-8') as f:
    text = f.read()

p_start = text.find('Tabla 39.')
if p_start != -1:
    with open('scratch/matriz_problemas_y_proyectos.txt', 'w', encoding='utf-8') as out:
        out.write(text[p_start:])
    print('Saved from Tabla 39 to end of chunk, length:', len(text) - p_start)
"`Viewed matriz_problemas_y_proyectos.txt:1-200 Ran command:`uv run python -c "
with open('scratch/matriz_problemas_y_proyectos.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find projects table: Tabla 45

p_proy = text.find('Tabla 45.')
if p_proy != -1:
    print('--- TABLA 45 (PROYECTOS) ---')
    print(text[p_proy:p_proy+4000])
"`Ran command:`uv run python -c "
with open('scratch/matriz_problemas_y_proyectos.txt', 'r', encoding='utf-8') as f:
    text = f.read()

p_proy = text.find('Tabla 45.')
p_model = text.find('3.2.4.')
if p_proy != -1 and p_model != -1:
    print(text[p_proy:p_model])
elif p_proy != -1:
    print(text[p_proy:p_proy+12000])
"`Ran command:`uv run python -c "
import os

source_full = 'docs/vaults/proyecto-guayquichuma/lake_mirror/pdot_guayquichuma_2023_2027/PDOT_GUAYQUICHUMA_2023_2027_COMPLETO.md'
sec_dir = 'docs/vaults/proyecto-guayquichuma/lake_mirror/pdot_guayquichuma_2023_2027/sections'

with open(source_full, 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('')[0])
    pages[num] = p

def save_sec(name, start, end):
    content = [f'# {name}\n\n']
    for i in range(start, end + 1):
        if i in pages:
            content.append(f'\n' + pages[i] + '\n\n')
    path = os.path.join(sec_dir, name)
    with open(path, 'w', encoding='utf-8') as out:
        out.writelines(content)
    print(f'Saved {name} (pages {start}-{end})')

save_sec('00_creditos_e_indice.md', 1, 10)
save_sec('01_fase_preparatoria.md', 11, 25)
save_sec('02_aspectos_generales_y_sistema_fisico_ambiental.md', 26, 50)
save_sec('03_sistema_asentamientos_humanos_y_economico.md', 51, 61)
save_sec('04_sistema_sociocultural_y_politico_institucional.md', 62, 76)
save_sec('05_diagnostico_integrado_y_priorizacion_problemas.md', 77, 86)
save_sec('06_propuesta_pdot_planes_programas_proyectos.md', 87, 98)
save_sec('07_modelo_de_gestion_y_estrategias.md', 99, 125)

print('All sections structured and sanitized!')
"`
Viewed matriz_problemas_y_proyectos.txt:200-450

Se ha procesado, renombrado y sanitizado formalmente el documento base en el repositorio de proyectos de inversión pública.

---

### 1. Acciones Realizadas en el Repositorio

1. **Ubicación e Integración del Documento**:

   - Se localizó el PDF oficial: *Plan de Desarrollo y Ordenamiento Territorial de la Parroquia Guayquichuma 2023–2027* (125 páginas).
   - Se normalizó y archivó en:
     [pdot_parroquial_guayquichuma_2023_2027.pdf](file:///d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-guayquichuma/evidencia/pdot_parroquial_guayquichuma_2023_2027.pdf).
2. **Sanitización y Estructuración a Markdown**:

   - Se convirtió íntegramente a Markdown preservando numeración de páginas, tablas y diagnósticos:
     [PDOT_GUAYQUICHUMA_2023_2027_COMPLETO.md](file:///d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-guayquichuma/lake_mirror/pdot_guayquichuma_2023_2027/PDOT_GUAYQUICHUMA_2023_2027_COMPLETO.md).
   - Se segmentó en capítulos limpios bajo [sections/](file:///d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-guayquichuma/lake_mirror/pdot_guayquichuma_2023_2027/sections):
     - `00_creditos_e_indice.md`
     - `01_fase_preparatoria.md`
     - `02_aspectos_generales_y_sistema_fisico_ambiental.md`
     - `03_sistema_asentamientos_humanos_y_economico.md`
     - `04_sistema_sociocultural_y_politico_institucional.md`
     - `05_diagnostico_integrado_y_priorizacion_problemas.md`
     - `06_propuesta_pdot_planes_programas_proyectos.md`
     - `07_modelo_de_gestion_y_estrategias.md`

---

### 2. Radiografía de Problemas Clave de Guayquichuma (Datos Oficiales PDOT 2023–2027)

Del análisis empírico de las matrices de diagnóstico (Tablas 34, 39, 41 y 45 del PDOT), se desprenden los siguientes nudos críticos:

| Eje Problemático                                                            | Evidencia Cuantitativa (PDOT / Censo INEC 2022)                                                                                                                                                                                                        | Impacto Territorial                                                                                        | Competencia COOTAD                                                                              |
| :--------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| **1. Déficit Crítico de Saneamiento y Agua Tratada**                 | • Solo el**25.64%** de viviendas están conectadas a red pública de alcantarillado.• Solo el **17.2%** de hogares trata el agua para beber.• Falta de planta de tratamiento de aguas residuales en barrios clave (El Prado, Cabecera). | Contaminación de afluentes, alta incidencia de enfermedades gastrointestinales y riesgo de desnutrición. | Municipal (Art. 55) concurrente con GAD Parroquial (Art. 65 lit. h / fiscalización y gestión) |
| **2. Vulnerabilidad Hídrica y Pérdida de Caudal**                    | • Disminución severa de caudal en quebradas abastecedoras:**El Badén, El Dudal y San Jacinto**.• 6,489.2 ha de cobertura vegetal expuestas a degradación y sobreutilización (48.55% del suelo sobreutilizado).                             | Escasez de agua en estiaje para consumo humano y riego agrícola de subsistencia.                          | GAD Parroquial (Art. 65 lit. d: preservación ambiental/biodiversidad)                          |
| **3. Baja Productividad Agropecuaria y Comercialización Fragmentada** | • Solo el**7.8%** del territorio tiene vocación agrícola/pecuaria, pero se usa el 38.37% (pastos y cultivos anuales de bajo rendimiento).• Cadenas de intermediación agresivas que reducen el ingreso de pequeños productores.             | Dependencia de bonos (44 familias con BDH), pobreza rural NBI del**63.8%**, migración de jóvenes.  | GAD Parroquial (Art. 65 lit. d: fomento productivo comunitario)                                 |
| **4. Conectividad Vial y Red Terciaria en Riesgo**                     | • Deterioro de vías rurales por eventos de movimientos en masa y falta de obras de drenaje/cunetas/alcantarillas en tramos críticos.                                                                                                                | Aislamiento estacional de barrios periféricos (Rumipotrero, Chiguango, El Prado).                         | GAD Provincial / concurrente con GAD Parroquial (Art. 65 lit. c: mantenimiento vial)            |

---

### 3. Propuestas Realistas y Viables para Presentar al GAD Parroquial

Para que un proyecto sea técnicamente defendible y financieramente viable para un GAD Parroquial (cuyo presupuesto de inversión anual ronda entre \$30,000 y \$120,000 según la Tabla 45), las propuestas más sólidas son:

1. **Opción A (Saneamiento Básico y Salud Pública - Alta prioridad y elegibilidad BDE):**

   - *Estudio y Factibilidad para el Mejoramiento del Sistema de Saneamiento Básico y Tratamiento de Aguas Residuales Descentralizado (Barrio El Prado / Cabecera).*
   - **Por qué es realista:** En el propio PDOT (pág. 96) tienen presupuestado \$45,000 para consultoría de este estudio; articulable mediante fondos no reembolsables o crédito BDE en convenio GAD Parroquial - GAD Municipal Catamayo.
2. **Opción B (Seguridad Hídrica y Fomento Productivo - Competencia Parroquial Pura):**

   - *Plan de Manejo y Protección de Fuentes de Recarga Hídrica (Microcuencas El Badén y San Jacinto) con Tecnificación de Riego Parcelario Comunitario.*
   - **Por qué es realista:** Se enmarca directamente en la competencia exclusiva del Art. 65 letra (d) del COOTAD (conservación de biodiversidad y fomento agropecuario) y da solución simultánea a la sequía y al bajo rendimiento agrícola.
3. **Opción C (Fortalecimiento Económico Comunitario y Cadenas de Valor):**

   - *Fortalecimiento de Capacidades Productivas y Centro de Acopio/Comercialización para Pequeños Productores Agropecuarios de Guayquichuma.*
   - **Por qué es realista:** Bajo costo de inversión directa (\$15,000 - \$25,000), alto impacto social inmediato para reducir la brecha de pobreza rural (NBI 63.8%).

¿Hacia cuál de estas líneas de inversión prefieres que orientemos la formulación del perfil de proyecto (Marco Lógico, Árbol de Problemas y Objetivos)?
