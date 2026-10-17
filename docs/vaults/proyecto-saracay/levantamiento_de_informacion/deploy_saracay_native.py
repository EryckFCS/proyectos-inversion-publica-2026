import requests
import json
import uuid

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

def make_kuid():
    return uuid.uuid4().hex[:8]

survey_raw = [
    # Metadatos automáticos
    {"name": "start", "type": "start", "$kuid": make_kuid(), "$xpath": "start", "$autoname": "start"},
    {"name": "end", "type": "end", "$kuid": make_kuid(), "$xpath": "end", "$autoname": "end"},
    {"name": "today", "type": "today", "$kuid": make_kuid(), "$xpath": "today", "$autoname": "today"},
    {"name": "username", "type": "username", "$kuid": make_kuid(), "$xpath": "username", "$autoname": "username"},
    
    # Módulo 0
    {"name": "grp_control", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 0: Metadatos y Control de la Entrevista"], "$qpath": "grp_control", "$xpath": "grp_control", "required": False, "$autoname": "grp_control"},
    {"name": "encuestador", "type": "text", "$kuid": make_kuid(), "label": ["Nombre del Encuestador / Investigador UNL"], "hint": ["Erick Condoy, David Pérez, Camila Correa, Luis Hurtado"], "$qpath": "grp_control/encuestador", "$xpath": "grp_control/encuestador", "required": True, "$autoname": "encuestador"},
    {"name": "fecha_entrevista", "type": "date", "$kuid": make_kuid(), "label": ["Fecha de la entrevista"], "$qpath": "grp_control/fecha_entrevista", "$xpath": "grp_control/fecha_entrevista", "required": True, "$autoname": "fecha_entrevista"},
    {"name": "gps_punto", "type": "geopoint", "$kuid": make_kuid(), "label": ["Ubicación geográfica GPS del punto de levantamiento"], "hint": ["Capture coordenadas en terreno con precisión GPS"], "$qpath": "grp_control/gps_punto", "$xpath": "grp_control/gps_punto", "required": False, "$autoname": "gps_punto"},
    {"name": "sector_saracay", "type": "select_one", "select_from_list_name": "list_sectores", "$kuid": make_kuid(), "label": ["Sector, Ciudadela o Recinto de Saracay (Piñas, El Oro)"], "$qpath": "grp_control/sector_saracay", "$xpath": "grp_control/sector_saracay", "required": True, "$autoname": "sector_saracay"},
    {"name": "sector_otro", "type": "text", "$kuid": make_kuid(), "label": ["Especifique el nombre del sector o recinto"], "$qpath": "grp_control/sector_otro", "$xpath": "grp_control/sector_otro", "required": False, "$autoname": "sector_otro"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 1
    {"name": "grp_informante", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 1: Perfil del Informante Clave"], "$qpath": "grp_informante", "$xpath": "grp_informante", "required": False, "$autoname": "grp_informante"},
    {"name": "nombre_informante", "type": "text", "$kuid": make_kuid(), "label": ["Nombre completo del informante"], "$qpath": "grp_informante/nombre_informante", "$xpath": "grp_informante/nombre_informante", "required": True, "$autoname": "nombre_informante"},
    {"name": "rol_comunidad", "type": "select_one", "select_from_list_name": "list_roles", "$kuid": make_kuid(), "label": ["Cargo o función principal en Saracay"], "$qpath": "grp_informante/rol_comunidad", "$xpath": "grp_informante/rol_comunidad", "required": True, "$autoname": "rol_comunidad"},
    {"name": "rol_otro", "type": "text", "$kuid": make_kuid(), "label": ["Especifique su cargo u ocupación"], "$qpath": "grp_informante/rol_otro", "$xpath": "grp_informante/rol_otro", "required": False, "$autoname": "rol_otro"},
    {"name": "rango_edad", "type": "select_one", "select_from_list_name": "list_edad", "$kuid": make_kuid(), "label": ["Rango de edad del informante"], "$qpath": "grp_informante/rango_edad", "$xpath": "grp_informante/rango_edad", "required": True, "$autoname": "rango_edad"},
    {"name": "tiempo_residencia", "type": "integer", "$kuid": make_kuid(), "label": ["¿Cuántos años reside en la Parroquia Saracay?"], "hint": ["Años continuos de residencia"], "$qpath": "grp_informante/tiempo_residencia", "$xpath": "grp_informante/tiempo_residencia", "required": True, "$autoname": "tiempo_residencia"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 2
    {"name": "grp_servicios", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 2: Diagnóstico de Agua, Saneamiento y Residuos"], "$qpath": "grp_servicios", "$xpath": "grp_servicios", "required": False, "$autoname": "grp_servicios"},
    {"name": "calidad_agua", "type": "select_one", "select_from_list_name": "list_calidad_agua", "$kuid": make_kuid(), "label": ["¿Cómo califica la calidad y servicio de agua de consumo en su sector?"], "$qpath": "grp_servicios/calidad_agua", "$xpath": "grp_servicios/calidad_agua", "required": True, "$autoname": "calidad_agua"},
    {"name": "continuidad_agua", "type": "select_one", "select_from_list_name": "list_continuidad", "$kuid": make_kuid(), "label": ["Continuidad del servicio de agua durante el día"], "$qpath": "grp_servicios/continuidad_agua", "$xpath": "grp_servicios/continuidad_agua", "required": True, "$autoname": "continuidad_agua"},
    {"name": "sistema_saneamiento", "type": "select_one", "select_from_list_name": "list_saneamiento", "$kuid": make_kuid(), "label": ["Tipo de sistema para evacuación de aguas servidas / excretas en su vivienda"], "$qpath": "grp_servicios/sistema_saneamiento", "$xpath": "grp_servicios/sistema_saneamiento", "required": True, "$autoname": "sistema_saneamiento"},
    {"name": "frecuencia_basura", "type": "select_one", "select_from_list_name": "list_recoleccion", "$kuid": make_kuid(), "label": ["Frecuencia de recolección de basura (GAD Municipal de Piñas)"], "$qpath": "grp_servicios/frecuencia_basura", "$xpath": "grp_servicios/frecuencia_basura", "required": True, "$autoname": "frecuencia_basura"},
    {"name": "problemas_saneamiento_obs", "type": "text", "$kuid": make_kuid(), "label": ["Principales deficiencias identificadas (turbiedad en invierno, cortes, vertidos sin PTAR al río Saracay)"], "$qpath": "grp_servicios/problemas_saneamiento_obs", "$xpath": "grp_servicios/problemas_saneamiento_obs", "required": False, "$autoname": "problemas_saneamiento_obs"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 3
    {"name": "grp_vialidad", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 3: Vialidad y Conectividad Territorial"], "$qpath": "grp_vialidad", "$xpath": "grp_vialidad", "required": False, "$autoname": "grp_vialidad"},
    {"name": "estado_vias_acceso", "type": "select_one", "select_from_list_name": "list_vias", "$kuid": make_kuid(), "label": ["Estado de las vías y accesos hacia su sector o recinto"], "$qpath": "grp_vialidad/estado_vias_acceso", "$xpath": "grp_vialidad/estado_vias_acceso", "required": True, "$autoname": "estado_vias_acceso"},
    {"name": "acceso_internet", "type": "select_one", "select_from_list_name": "list_internet", "$kuid": make_kuid(), "label": ["Acceso a conectividad de internet"], "$qpath": "grp_vialidad/acceso_internet", "$xpath": "grp_vialidad/acceso_internet", "required": True, "$autoname": "acceso_internet"},
    {"name": "afectacion_crecidas", "type": "select_one", "select_from_list_name": "list_sino", "$kuid": make_kuid(), "label": ["¿Su sector o cultivos sufren daños por deslizamientos o crecidas del río Saracay en invierno?"], "$qpath": "grp_vialidad/afectacion_crecidas", "$xpath": "grp_vialidad/afectacion_crecidas", "required": True, "$autoname": "afectacion_crecidas"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 4
    {"name": "grp_productivo", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 4: Sistema Económico y Productivo"], "$qpath": "grp_productivo", "$xpath": "grp_productivo", "required": False, "$autoname": "grp_productivo"},
    {"name": "actividades_ingresos", "type": "select_multiple", "select_from_list_name": "list_actividades", "$kuid": make_kuid(), "label": ["Principales actividades económicas generadoras de ingresos (Selección múltiple)"], "$qpath": "grp_productivo/actividades_ingresos", "$xpath": "grp_productivo/actividades_ingresos", "required": True, "$autoname": "actividades_ingresos"},
    {"name": "canal_comercializacion", "type": "select_one", "select_from_list_name": "list_comercializacion", "$kuid": make_kuid(), "label": ["Canal principal de venta de sus productos"], "$qpath": "grp_productivo/canal_comercializacion", "$xpath": "grp_productivo/canal_comercializacion", "required": True, "$autoname": "canal_comercializacion"},
    {"name": "percepcion_turismo_la_y", "type": "select_one", "select_from_list_name": "list_nivel", "$kuid": make_kuid(), "label": ["Potencial comercial y turístico del sector La Y de Saracay"], "$qpath": "grp_productivo/percepcion_turismo_la_y", "$xpath": "grp_productivo/percepcion_turismo_la_y", "required": True, "$autoname": "percepcion_turismo_la_y"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 5
    {"name": "grp_prioridades", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 5: Prioridades de Inversión Pública para Saracay"], "$qpath": "grp_prioridades", "$xpath": "grp_prioridades", "required": False, "$autoname": "grp_prioridades"},
    {"name": "prioridad_1_obra", "type": "select_one", "select_from_list_name": "list_prioridades", "$kuid": make_kuid(), "label": ["PRIORIDAD #1: Proyecto u obra pública más urgente para la parroquia"], "$qpath": "grp_prioridades/prioridad_1_obra", "$xpath": "grp_prioridades/prioridad_1_obra", "required": True, "$autoname": "prioridad_1_obra"},
    {"name": "prioridad_2_obra", "type": "select_one", "select_from_list_name": "list_prioridades", "$kuid": make_kuid(), "label": ["PRIORIDAD #2: Segunda obra prioritaria para Saracay"], "$qpath": "grp_prioridades/prioridad_2_obra", "$xpath": "grp_prioridades/prioridad_2_obra", "required": True, "$autoname": "prioridad_2_obra"},
    {"name": "obras_en_ejecucion", "type": "text", "$kuid": make_kuid(), "label": ["Obras o proyectos públicos que conozca actualmente en ejecución en la parroquia"], "$qpath": "grp_prioridades/obras_en_ejecucion", "$xpath": "grp_prioridades/obras_en_ejecucion", "required": False, "$autoname": "obras_en_ejecucion"},
    {"name": "foto_evidencia", "type": "image", "$kuid": make_kuid(), "label": ["Fotografía de evidencia de la visita o infraestructura (Opcional)"], "$qpath": "grp_prioridades/foto_evidencia", "$xpath": "grp_prioridades/foto_evidencia", "required": False, "$autoname": "foto_evidencia"},
    {"name": "nota_cierre", "type": "note", "$kuid": make_kuid(), "label": ["Muchas gracias por su colaboración con la Universidad Nacional de Loja y el diagnóstico territorial de la Parroquia Saracay (Piñas, El Oro)."], "$qpath": "grp_prioridades/nota_cierre", "$xpath": "grp_prioridades/nota_cierre", "required": False, "$autoname": "nota_cierre"},
    {"type": "end_group", "$kuid": make_kuid()}
]

choices_raw = [
    # list_sectores
    {"list_name": "list_sectores", "name": "cabecera_central", "label": ["Cabecera Parroquial - Sector Central"], "$kuid": make_kuid(), "$autovalue": "cabecera_central"},
    {"list_name": "list_sectores", "name": "la_y_saracay", "label": ["Sector La Y de Saracay (Nodo vial E585 / E25)"], "$kuid": make_kuid(), "$autovalue": "la_y_saracay"},
    {"list_name": "list_sectores", "name": "el_bosque", "label": ["Ciudadela El Bosque"], "$kuid": make_kuid(), "$autovalue": "el_bosque"},
    {"list_name": "list_sectores", "name": "el_tamarindo", "label": ["Ciudadela El Tamarindo"], "$kuid": make_kuid(), "$autovalue": "el_tamarindo"},
    {"list_name": "list_sectores", "name": "la_inmaculada", "label": ["Ciudadela La Inmaculada"], "$kuid": make_kuid(), "$autovalue": "la_inmaculada"},
    {"list_name": "list_sectores", "name": "las_brisas", "label": ["Ciudadela Las Brisas"], "$kuid": make_kuid(), "$autovalue": "las_brisas"},
    {"list_name": "list_sectores", "name": "platanillos", "label": ["Recinto Platanillos"], "$kuid": make_kuid(), "$autovalue": "platanillos"},
    {"list_name": "list_sectores", "name": "panupali", "label": ["Recinto Panupali"], "$kuid": make_kuid(), "$autovalue": "panupali"},
    {"list_name": "list_sectores", "name": "naranjos", "label": ["Recinto Naranjos"], "$kuid": make_kuid(), "$autovalue": "naranjos"},
    {"list_name": "list_sectores", "name": "san_jose", "label": ["Recinto San José"], "$kuid": make_kuid(), "$autovalue": "san_jose"},
    {"list_name": "list_sectores", "name": "fatima", "label": ["Recinto Fátima"], "$kuid": make_kuid(), "$autovalue": "fatima"},
    {"list_name": "list_sectores", "name": "damas", "label": ["Recinto Damas"], "$kuid": make_kuid(), "$autovalue": "damas"},
    {"list_name": "list_sectores", "name": "otro", "label": ["Otro recinto / comunidad"], "$kuid": make_kuid(), "$autovalue": "otro"},

    # list_roles
    {"list_name": "list_roles", "name": "presidente_gad", "label": ["Presidente del GAD Parroquial (Sr. Jorge Homero Ochoa Sánchez)"], "$kuid": make_kuid(), "$autovalue": "presidente_gad"},
    {"list_name": "list_roles", "name": "vocal_gad", "label": ["Vocal o funcionario del GAD Parroquial"], "$kuid": make_kuid(), "$autovalue": "vocal_gad"},
    {"list_name": "list_roles", "name": "lider_comunitario", "label": ["Líder comunitario / Representante de recinto"], "$kuid": make_kuid(), "$autovalue": "lider_comunitario"},
    {"list_name": "list_roles", "name": "salud_educacion", "label": ["Personal de salud o directivo docente"], "$kuid": make_kuid(), "$autovalue": "salud_educacion"},
    {"list_name": "list_roles", "name": "productor_agropecuario", "label": ["Productor agropecuario (Caña, Maíz, Ganadería, Cacao)"], "$kuid": make_kuid(), "$autovalue": "productor_agropecuario"},
    {"list_name": "list_roles", "name": "comerciante_gastronomico", "label": ["Comerciante / Emprendedor gastronómico en La Y"], "$kuid": make_kuid(), "$autovalue": "comerciante_gastronomico"},
    {"list_name": "list_roles", "name": "morador", "label": ["Habitante / Morador de la parroquia"], "$kuid": make_kuid(), "$autovalue": "morador"},
    {"list_name": "list_roles", "name": "otro", "label": ["Otro"], "$kuid": make_kuid(), "$autovalue": "otro"},

    # list_edad
    {"list_name": "list_edad", "name": "18_29", "label": ["18 a 29 años"], "$kuid": make_kuid(), "$autovalue": "18_29"},
    {"list_name": "list_edad", "name": "30_45", "label": ["30 a 45 años"], "$kuid": make_kuid(), "$autovalue": "30_45"},
    {"list_name": "list_edad", "name": "46_60", "label": ["46 a 60 años"], "$kuid": make_kuid(), "$autovalue": "46_60"},
    {"list_name": "list_edad", "name": "mas_60", "label": ["Más de 60 años"], "$kuid": make_kuid(), "$autovalue": "mas_60"},

    # list_calidad_agua
    {"list_name": "list_calidad_agua", "name": "buena", "label": ["Buena (tratada / apta para consumo)"], "$kuid": make_kuid(), "$autovalue": "buena"},
    {"list_name": "list_calidad_agua", "name": "regular_entubada", "label": ["Regular (agua entubada sin cloración constante)"], "$kuid": make_kuid(), "$autovalue": "regular_entubada"},
    {"list_name": "list_calidad_agua", "name": "vertiente_quebrada", "label": ["Vertiente / Quebrada sin tratamiento"], "$kuid": make_kuid(), "$autovalue": "vertiente_quebrada"},
    {"list_name": "list_calidad_agua", "name": "tanquero_compra", "label": ["Compra de bidones / Tanquero"], "$kuid": make_kuid(), "$autovalue": "tanquero_compra"},

    # list_continuidad
    {"list_name": "list_continuidad", "name": "continua_24h", "label": ["Continua las 24 horas del día"], "$kuid": make_kuid(), "$autovalue": "continua_24h"},
    {"list_name": "list_continuidad", "name": "parcial_horas", "label": ["Parcial (ciertas horas al día)"], "$kuid": make_kuid(), "$autovalue": "parcial_horas"},
    {"list_name": "list_continuidad", "name": "cortes_frecuentes", "label": ["Intermitente con cortes frecuentes en invierno/verano"], "$kuid": make_kuid(), "$autovalue": "cortes_frecuentes"},

    # list_saneamiento
    {"list_name": "list_saneamiento", "name": "alcantarillado", "label": ["Red pública de alcantarillado sanitario"], "$kuid": make_kuid(), "$autovalue": "alcantarillado"},
    {"list_name": "list_saneamiento", "name": "pozo_septico", "label": ["Pozo séptico individual"], "$kuid": make_kuid(), "$autovalue": "pozo_septico"},
    {"list_name": "list_saneamiento", "name": "pozo_ciego_letrina", "label": ["Pozo ciego / Letrina"], "$kuid": make_kuid(), "$autovalue": "pozo_ciego_letrina"},
    {"list_name": "list_saneamiento", "name": "descarga_rio", "label": ["Descarga directa a estero, quebrada o río Saracay"], "$kuid": make_kuid(), "$autovalue": "descarga_rio"},

    # list_recoleccion
    {"list_name": "list_recoleccion", "name": "diario", "label": ["Diario"], "$kuid": make_kuid(), "$autovalue": "diario"},
    {"list_name": "list_recoleccion", "name": "dos_tres_semana", "label": ["2 a 3 veces por semana"], "$kuid": make_kuid(), "$autovalue": "dos_tres_semana"},
    {"list_name": "list_recoleccion", "name": "semanal", "label": ["1 vez por semana"], "$kuid": make_kuid(), "$autovalue": "semanal"},
    {"list_name": "list_recoleccion", "name": "irregular_quema", "label": ["No pasa recolector (quema o entierro)"], "$kuid": make_kuid(), "$autovalue": "irregular_quema"},

    # list_vias
    {"list_name": "list_vias", "name": "asfaltada_buena", "label": ["Asfaltada en buen estado (Eje principal E585)"], "$kuid": make_kuid(), "$autovalue": "asfaltada_buena"},
    {"list_name": "list_vias", "name": "lastrada_regular", "label": ["Lastrada / Afirmada con baches"], "$kuid": make_kuid(), "$autovalue": "lastrada_regular"},
    {"list_name": "list_vias", "name": "critica_invierno", "label": ["Mala / Intransitable en temporada lluviosa"], "$kuid": make_kuid(), "$autovalue": "critica_invierno"},

    # list_internet
    {"list_name": "list_internet", "name": "fibra", "label": ["Fibra óptica domiciliaria"], "$kuid": make_kuid(), "$autovalue": "fibra"},
    {"list_name": "list_internet", "name": "datos_moviles", "label": ["Datos móviles celular"], "$kuid": make_kuid(), "$autovalue": "datos_moviles"},
    {"list_name": "list_internet", "name": "sin_acceso", "label": ["Sin acceso a internet"], "$kuid": make_kuid(), "$autovalue": "sin_acceso"},

    # list_sino
    {"list_name": "list_sino", "name": "si", "label": ["Sí"], "$kuid": make_kuid(), "$autovalue": "si"},
    {"list_name": "list_sino", "name": "no", "label": ["No"], "$kuid": make_kuid(), "$autovalue": "no"},

    # list_actividades
    {"list_name": "list_actividades", "name": "cana_panela", "label": ["Cultivo de caña de azúcar y molienda de panela"], "$kuid": make_kuid(), "$autovalue": "cana_panela"},
    {"list_name": "list_actividades", "name": "maiz_granos", "label": ["Producción de maíz duro y granos"], "$kuid": make_kuid(), "$autovalue": "maiz_granos"},
    {"list_name": "list_actividades", "name": "platano_cacao", "label": ["Plátano y cacao fino de aroma"], "$kuid": make_kuid(), "$autovalue": "platano_cacao"},
    {"list_name": "list_actividades", "name": "ganaderia_carne_leche", "label": ["Ganadería bovina de carne y leche"], "$kuid": make_kuid(), "$autovalue": "ganaderia_carne_leche"},
    {"list_name": "list_actividades", "name": "comercio_gastronomia_la_y", "label": ["Comercio gastronómico y paradores en La Y"], "$kuid": make_kuid(), "$autovalue": "comercio_gastronomia_la_y"},
    {"list_name": "list_actividades", "name": "transporte_servicios", "label": ["Transporte interprovincial, mecánica y servicios"], "$kuid": make_kuid(), "$autovalue": "transporte_servicios"},

    # list_comercializacion
    {"list_name": "list_comercializacion", "name": "venta_la_y", "label": ["Venta directa en paradores de La Y de Saracay"], "$kuid": make_kuid(), "$autovalue": "venta_la_y"},
    {"list_name": "list_comercializacion", "name": "mercados_pinas_balsas", "label": ["Mercados cantonales (Piñas, Balsas o Machala)"], "$kuid": make_kuid(), "$autovalue": "mercados_pinas_balsas"},
    {"list_name": "list_comercializacion", "name": "intermediario_finca", "label": ["Intermediario a pie de finca"], "$kuid": make_kuid(), "$autovalue": "intermediario_finca"},
    {"list_name": "list_comercializacion", "name": "consumo_local", "label": ["Consumo familiar y venta menor"], "$kuid": make_kuid(), "$autovalue": "consumo_local"},

    # list_nivel
    {"list_name": "list_nivel", "name": "alto", "label": ["Alto"], "$kuid": make_kuid(), "$autovalue": "alto"},
    {"list_name": "list_nivel", "name": "medio", "label": ["Medio"], "$kuid": make_kuid(), "$autovalue": "medio"},
    {"list_name": "list_nivel", "name": "bajo", "label": ["Bajo"], "$kuid": make_kuid(), "$autovalue": "bajo"},

    # list_prioridades
    {"list_name": "list_prioridades", "name": "alcantarillado_ptar", "label": ["Alcantarillado sanitario y Planta de Tratamiento de Aguas Residuales (PTAR)"], "$kuid": make_kuid(), "$autovalue": "alcantarillado_ptar"},
    {"list_name": "list_prioridades", "name": "agua_potable_optimizacion", "label": ["Optimización y ampliación de reservorios de agua potable"], "$kuid": make_kuid(), "$autovalue": "agua_potable_optimizacion"},
    {"list_name": "list_prioridades", "name": "vias_recintos", "label": ["Asfaltado y mejoramiento vial a recintos (Platanillos, Panupali)"], "$kuid": make_kuid(), "$autovalue": "vias_recintos"},
    {"list_name": "list_prioridades", "name": "ordenamiento_la_y", "label": ["Ordenamiento urbano, drenaje y parador turístico en La Y"], "$kuid": make_kuid(), "$autovalue": "ordenamiento_la_y"},
    {"list_name": "list_prioridades", "name": "salud_equipamiento", "label": ["Ampliación y equipamiento del Centro de Salud"], "$kuid": make_kuid(), "$autovalue": "salud_equipamiento"},
    {"list_name": "list_prioridades", "name": "defensas_rio", "label": ["Muros de contención y defensas ribereñas en el río Saracay"], "$kuid": make_kuid(), "$autovalue": "defensas_rio"}
]

payload_asset = {
    "name": "Encuesta Diagnóstico Territorial Saracay - UNL",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": survey_raw,
        "choices": choices_raw,
        "settings": {
            "style": "theme-grid",
            "default_language": "Español (español)"
        },
        "translated": ["label", "hint"],
        "translations": ["Español (español)"]
    })
}

print("1. Creando Formulario Oficial Saracay...")
r_create = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=payload_asset)
print("Create Status:", r_create.status_code)
uid = r_create.json().get("uid")
print("UID:", uid)

print("2. Desplegando Formulario Oficial...")
r_dep = requests.post(
    f"{BASE_URL}/api/v2/assets/{uid}/deployment/",
    headers=headers_dep,
    data={"active": "true"}
)
print("Deploy Status:", r_dep.status_code)

if r_dep.status_code in [200, 201]:
    r_final = requests.get(f"{BASE_URL}/api/v2/assets/{uid}/", headers=headers)
    links = r_final.json().get("deployment__links", {})
    print("\n" + "="*70)
    print("¡ENLACES OFICIALES KOBOTOOLBOX - PARROQUIA SARACAY!")
    print(f"UID del Formulario: {uid}")
    print(f"URL Web Enketo (Online): {links.get('url')}")
    print(f"URL Envío Único: {links.get('single_url')}")
    print(f"URL Offline: {links.get('offline_url')}")
    print("="*70)
else:
    print("Deploy text:", r_dep.text[:400])
