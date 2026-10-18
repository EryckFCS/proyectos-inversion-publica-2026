import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import shutil
import os

doc = docx.Document()

# Margenes
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Estilo base
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x33, 0x33, 0x33)

def add_header(title, level=1):
    h = doc.add_heading(title, level=level)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    return h

# Titulo Principal
p_uni = doc.add_paragraph()
p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
r1 = p_uni.add_run('UNIVERSIDAD NACIONAL DE LOJA\nFACULTAD JURÍDICA, SOCIAL Y ADMINISTRATIVA\nCARRERA DE ECONOMÍA\n')
r1.bold = True
r1.font.size = Pt(13)
r1.font.color.rgb = RGBColor(0x0a, 0x3d, 0x62)

r2 = p_uni.add_run('LEVANTAMIENTO DE INDICADORES TERRITORIALES (40 VARIABLES)\nPROYECTO DE INVERSIÓN PÚBLICA: PARROQUIA RURAL TORATA (EL ORO)')
r2.bold = True
r2.font.size = Pt(12)
r2.font.color.rgb = RGBColor(0x1e, 0x37, 0x99)

p_meta = doc.add_paragraph('Asignatura: Proyectos de Inversión Pública (Séptimo Ciclo)\nDirector de Carrera: Econ. José Job Chamba Tandazo\nFecha: Octubre de 2026')
p_meta.paragraph_format.space_after = Pt(12)

def create_table(headers, data):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        # Background
        shading = OxmlElement('w:shd')
        shading.set(qn('w:val'), 'clear')
        shading.set(qn('w:color'), 'auto')
        shading.set(qn('w:fill'), '1e3799')
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)
        
    for r_idx, row in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx <= 1 else WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(9)
            if r_idx % 2 == 1:
                shading = OxmlElement('w:shd')
                shading.set(qn('w:val'), 'clear')
                shading.set(qn('w:color'), 'auto')
                shading.set(qn('w:fill'), 'F1F2F6')
                row_cells[c_idx]._tc.get_or_add_tcPr().append(shading)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

# 1. Datos del Territorio
add_header('1. DATOS GENERALES DEL TERRITORIO', 2)
headers_gen = ['Variable', 'Unidad de Medida', 'Valor / Indicador Oficial']
data_gen = [
    ['División político-administrativa', 'Categórica', 'Parroquia rural Torata, Cantón Santa Rosa, Prov. El Oro'],
    ['Instrumentos vigentes', 'Nombre oficial', 'PDOT Torata 2023-2027 (Res. GADPR-T-014-2024); PDOT Santa Rosa'],
    ['Ubicación geográfica cabecera', 'WGS84', 'Lat: -3.5650, Lon: -79.8820 (3°33\'54" S, 79°52\'55" W)'],
    ['Superficie total parroquial', 'ha / km²', '8.538,00 ha (85,38 km²)'],
    ['Altitud media', 'msnm', '420 a 1.250 msnm (Cabecera: ~480 msnm)'],
    ['Temperatura media anual', '°C', '22,4 °C a 24,8 °C (Subtropical templado-cálido)'],
    ['Precipitación media anual', 'mm/año', '1.150 a 1.450 mm/año'],
    ['Uso económico predominante', '% del suelo', 'Pastos/Ganadería (58,4%), Bosque/Vegetación (27,2%), Cultivos (11,8%)'],
    ['Red vial y estado de acceso', 'km y %', '46,2 km (34% Asfaltada E585 en buen estado; 48% Lastrada; 18% Verano)'],
    ['Centros poblados identificados', 'Número', '8 asentamientos (Torata, El Playón, La Chilca, Sabayán, El Guayabo, etc.)'],
    ['Población total área intervención', 'Habitantes', '2.174 hab. (Censo INEC 2022)'],
    ['Densidad poblacional', 'hab/km²', '25,46 hab/km²'],
    ['Tasa de crecimiento intercensal', '% anual', '0,94 % anual'],
    ['Tiempo de acceso cabecera cantonal', 'Minutos', '40 minutos (hacia Santa Rosa vía E585 - La Avanzada)']
]
create_table(headers_gen, data_gen)

# 2. Diagnostico Territorial 40 Variables
add_header('2. MATRIZ DE DIAGNÓSTICO TERRITORIAL (40 VARIABLES)', 2)

headers_diag = ['Componente', 'Variable', 'Unidad', 'Valor Oficial', 'Fuente']
data_diag = [
    ['SOCIAL', 'Población masculina', 'Habitantes (%)', '1.109 hab (51,01%)', 'INEC 2022'],
    ['SOCIAL', 'Población femenina', 'Habitantes (%)', '1.065 hab (48,99%)', 'INEC 2022'],
    ['SOCIAL', 'Densidad poblacional', 'hab/km²', '25,46 hab/km²', 'PDOT Torata'],
    ['SOCIAL', 'Estructura 0 a 14 años', '%', '24,80 %', 'INEC 2022'],
    ['SOCIAL', 'Estructura 15 a 64 años', '%', '63,10 %', 'INEC 2022'],
    ['SOCIAL', 'Estructura 65 años y más', '%', '12,10 %', 'INEC 2022'],
    ['SOCIAL', 'Autoidentificación mestiza', '%', '92,40 %', 'INEC 2022'],
    ['SOCIAL', 'Autoidentificación otras etnias', '%', '7,60 %', 'INEC 2022'],
    ['SOCIAL', 'Tasa crecimiento poblacional', '% anual', '0,94 %', 'INEC 2022'],
    ['SOCIAL', 'Escolaridad promedio', 'Años', '7,8 años', 'INEC 2022'],
    ['SOCIAL', 'Tasa de alfabetización', '%', '92,60 %', 'INEC 2022'],
    ['SOCIAL', 'Pobreza por NBI', '%', '67,40 %', 'INEC / PDOT'],
    ['SOCIAL', 'Cobertura agua red/entubada', '% viviendas', '64,20 %', 'EMAPASR-EP'],
    ['SOCIAL', 'Cobertura alcantarillado sanitario', '% viviendas', '28,50 %', 'EMAPASR-EP'],
    ['SOCIAL', 'Letrina / pozo ciego / sin sistema', '% viviendas', '71,50 %', 'EMAPASR-EP'],
    ['SOCIAL', 'Cobertura energía eléctrica', '% viviendas', '95,80 %', 'CNEL El Oro'],
    ['SOCIAL', 'Recolección de residuos', '% viviendas', '54,30 %', 'GAD Santa Rosa'],
    ['SOCIAL', 'Cobertura internet fijo', '% hogares', '38,70 %', 'INEC 2022'],
    ['SOCIAL', 'Establecimientos educativos', 'Número', '4 unidades', 'Min. Educación'],
    ['SOCIAL', 'Establecimientos de salud', 'Número', '1 Centro Tipo A', 'MSP 07D06'],
    ['SOCIAL', 'Tiempo acceso centro urbano', 'Minutos', '40 minutos', 'GADPR Torata'],
    ['SOCIAL', 'Longitud red vial', 'km', '46,20 km', 'MTOP / GAD'],
    ['SOCIAL', 'Vías pavimentadas/asfaltadas', '%', '34,20 %', 'PDOT Torata'],
    ['ECONÓMICO', 'PEA', 'Personas (%)', '985 hab (45,3%)', 'INEC 2022'],
    ['ECONÓMICO', 'Tasa empleo asalariado/adecuado', '%', '31,40 %', 'PDOT Santa Rosa'],
    ['ECONÓMICO', 'Tasa subempleo / jornalero', '%', '63,20 %', 'PDOT Santa Rosa'],
    ['ECONÓMICO', 'Tasa de desempleo abierto', '%', '5,40 %', 'INEC 2022'],
    ['ECONÓMICO', 'Sector primario agropecuario', '%', '68,50 %', 'PDOT Torata'],
    ['ECONÓMICO', 'Sector servicios y comercio', '%', '21,30 %', 'PDOT Torata'],
    ['ECONÓMICO', 'Construcción / manufactura', '%', '10,20 %', 'PDOT Torata'],
    ['ECONÓMICO', 'Unidades económicas SRI', 'Número', '42 unidades', 'SRI Santa Rosa'],
    ['ECONÓMICO', 'Ingreso promedio mensual hogar', 'USD/mes', '415,00 USD', 'Encuesta GAD'],
    ['ECONÓMICO', 'Producción ganadera bovina', 'Cabezas', '~4.800 cabezas', 'MAG / Agrocalidad'],
    ['ECONÓMICO', 'Producción agrícola comercial', 'toneladas/año', '~1.650 ton/año', 'MAG El Oro'],
    ['ECONÓMICO', 'Llegada de excursionistas', 'Personas/año', '~1.200 hab/año', 'Turismo GAD'],
    ['ECONÓMICO', 'Superficie uso agropecuario', 'ha', '5.240 ha', 'MAG / PDOT'],
    ['AMBIENTAL', 'Superficie del área de estudio', 'ha', '8.538,00 ha', 'IGM / SIGTIERRAS'],
    ['AMBIENTAL', 'Altitud media', 'msnm', '480 msnm', 'SRTM'],
    ['AMBIENTAL', 'Pendiente media del territorio', '%', '28 %', 'PDOT Torata'],
    ['AMBIENTAL', 'Temperatura media anual', '°C', '23,6 °C', 'INAMHI'],
    ['AMBIENTAL', 'Precipitación media anual', 'mm/año', '1.280 mm/año', 'INAMHI'],
    ['AMBIENTAL', 'Bosque y cobertura natural', 'ha (%)', '2.322 ha (27,2%)', 'MAATE'],
    ['AMBIENTAL', 'Pastizales y pastos cultivados', 'ha (%)', '4.986 ha (58,4%)', 'MAG / MAATE'],
    ['AMBIENTAL', 'Zonas recarga hídrica río Santa Rosa', 'ha', '1.450 ha', 'EMAPASR-EP'],
    ['AMBIENTAL', 'Área expuesta a deslizamientos', 'ha (%)', '1.840 ha (21,5%)', 'SNGRE'],
    ['AMBIENTAL', 'Amenazas prioritarias', 'Número', '2 (Taludes / Inund)', 'Plan Contingencia'],
    ['AMBIENTAL', 'Caudal disponible tomas agua', 'L/s', '32,5 L/s', 'EMAPASR-EP'],
    ['INSTITUCIONAL', 'Organizaciones sociales constituidas', 'Número', '11 organizaciones', 'MIES / GAD'],
    ['INSTITUCIONAL', 'Presupuesto anual GAD Parroquial', 'USD/año', '~260.000 USD', 'Cédula GADPR'],
    ['INSTITUCIONAL', 'Proyectos ejecutados trienio', 'Número', '6 proyectos', 'Rendición Cuentas'],
    ['INSTITUCIONAL', 'Instrumentos de planificación', 'Número', '2 (PDOT y PUGS)', 'Registro Oficial'],
    ['INSTITUCIONAL', 'Instituciones con presencia territorial', 'Número', '6 entidades', 'Directorio GAD'],
    ['INSTITUCIONAL', 'Emprendimientos y cooperativas', 'Número', '5 unidades', 'MIPRO / GAD']
]
create_table(headers_diag, data_diag)

p_firm = doc.add_paragraph()
p_firm.paragraph_format.space_before = Pt(24)
p_firm.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_firm.add_run('_____________________________________________\nEcon. José Job Chamba Tandazo\nDIRECTOR DE LA CARRERA DE ECONOMÍA\nUNIVERSIDAD NACIONAL DE LOJA').bold = True

docx_path = r'd:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro/levantamiento_de_informacion/ficha_indicadores_territoriales.docx'
doc.save(docx_path)
print('DOCX generado exitosamente en:', docx_path)

site_docx = r'd:/07_Ciclo/septimo_ciclo/public_investment_projects/_site/docs/vaults/proyecto-torata-el_oro/levantamiento_de_informacion/ficha_indicadores_territoriales.docx'
shutil.copy2(docx_path, site_docx)
print('DOCX sincronizado con _site.')
