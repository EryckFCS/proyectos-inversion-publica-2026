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
    # Metadatos del sistema
    {"name": "start", "type": "start", "$kuid": make_kuid(), "$xpath": "start", "$autoname": "start"},
    {"name": "end", "type": "end", "$kuid": make_kuid(), "$xpath": "end", "$autoname": "end"},
    {"name": "today", "type": "today", "$kuid": make_kuid(), "$xpath": "today", "$autoname": "today"},
    {"name": "username", "type": "username", "$kuid": make_kuid(), "$xpath": "username", "$autoname": "username"},
    
    # Módulo 0: Metadatos y Control Institucional
    {"name": "grp_control", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 0: Metadatos y Registro Institucional"], "$qpath": "grp_control", "$xpath": "grp_control", "required": False, "$autoname": "grp_control"},
    {"name": "nota_autoridad", "type": "note", "$kuid": make_kuid(), "label": ["Entrevista de Diagnóstico Territorial y Línea Base de Inversión Pública dirigida a la Autoridad Local: Sr. Jorge Homero Ochoa Sánchez (Presidente del GAD Parroquial Rural de Saracay 2023-2027)."], "$qpath": "grp_control/nota_autoridad", "$xpath": "grp_control/nota_autoridad", "required": False, "$autoname": "nota_autoridad"},
    {"name": "encuestador", "type": "text", "$kuid": make_kuid(), "label": ["Nombre del Investigador / Entrevistador UNL"], "hint": ["Erick Condoy, David Pérez, Camila Correa, Luis Hurtado"], "$qpath": "grp_control/encuestador", "$xpath": "grp_control/encuestador", "required": True, "$autoname": "encuestador"},
    {"name": "fecha_entrevista", "type": "date", "$kuid": make_kuid(), "label": ["Fecha de la entrevista"], "$qpath": "grp_control/fecha_entrevista", "$xpath": "grp_control/fecha_entrevista", "required": True, "$autoname": "fecha_entrevista"},
    {"name": "gps_punto", "type": "geopoint", "$kuid": make_kuid(), "label": ["Ubicación geográfica GPS (Sede del GAD Parroquial)"], "hint": ["Capture coordenadas en terreno con el móvil"], "$qpath": "grp_control/gps_punto", "$xpath": "grp_control/gps_punto", "required": False, "$autoname": "gps_punto"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 1: Marco de Planificación y Territorio
    {"name": "grp_planificacion", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 1: Marco de Planificación y Delimitación Territorial"], "$qpath": "grp_planificacion", "$xpath": "grp_planificacion", "required": False, "$autoname": "grp_planificacion"},
    {"name": "estado_pdot", "type": "select_one", "select_from_list_name": "list_estado_pdot", "$kuid": make_kuid(), "label": ["Estado formal del Plan de Desarrollo y Ordenamiento Territorial (PDOT) de Saracay"], "$qpath": "grp_planificacion/estado_pdot", "$xpath": "grp_planificacion/estado_pdot", "required": True, "$autoname": "estado_pdot"},
    {"name": "recintos_criticos", "type": "text", "$kuid": make_kuid(), "label": ["Recintos o sectores rurales con mayores rezagos y necesidad de atención emergente"], "hint": ["Ej. Platanillos, Panupali, Naranjos, Damas, Fátima"], "$qpath": "grp_planificacion/recintos_criticos", "$xpath": "grp_planificacion/recintos_criticos", "required": True, "$autoname": "recintos_criticos"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 2: Saneamiento Básico, Agua y Residuos
    {"name": "grp_servicios", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 2: Diagnóstico de Agua Potable y Saneamiento"], "$qpath": "grp_servicios", "$xpath": "grp_servicios", "required": False, "$autoname": "grp_servicios"},
    {"name": "calidad_agua", "type": "select_one", "select_from_list_name": "list_calidad_agua", "$kuid": make_kuid(), "label": ["Situación de la calidad del agua de consumo en la cabecera parroquial"], "$qpath": "grp_servicios/calidad_agua", "$xpath": "grp_servicios/calidad_agua", "required": True, "$autoname": "calidad_agua"},
    {"name": "continuidad_agua", "type": "select_one", "select_from_list_name": "list_continuidad", "$kuid": make_kuid(), "label": ["Continuidad del suministro de agua durante el día"], "$qpath": "grp_servicios/continuidad_agua", "$xpath": "grp_servicios/continuidad_agua", "required": True, "$autoname": "continuidad_agua"},
    {"name": "sistema_saneamiento", "type": "select_one", "select_from_list_name": "list_saneamiento", "$kuid": make_kuid(), "label": ["Situación del alcantarillado sanitario y PTAR en la parroquia"], "$qpath": "grp_servicios/sistema_saneamiento", "$xpath": "grp_servicios/sistema_saneamiento", "required": True, "$autoname": "sistema_saneamiento"},
    {"name": "descargas_contaminantes", "type": "select_one", "select_from_list_name": "list_sino", "$kuid": make_kuid(), "label": ["¿Existen descargas crudas de aguas servidas directamente al río Saracay o afluentes?"], "$qpath": "grp_servicios/descargas_contaminantes", "$xpath": "grp_servicios/descargas_contaminantes", "required": True, "$autoname": "descargas_contaminantes"},
    {"name": "problemas_saneamiento_obs", "type": "text", "$kuid": make_kuid(), "label": ["Deficiencias prioritarias en agua y saneamiento"], "hint": ["Cortes de agua, turbiedad en invierno, falta de PTAR"], "$qpath": "grp_servicios/problemas_saneamiento_obs", "$xpath": "grp_servicios/problemas_saneamiento_obs", "required": False, "$autoname": "problemas_saneamiento_obs"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 3: Conectividad Vial y Riesgos
    {"name": "grp_vialidad", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 3: Vialidad, Conectividad y Gestión de Riesgos"], "$qpath": "grp_vialidad", "$xpath": "grp_vialidad", "required": False, "$autoname": "grp_vialidad"},
    {"name": "estado_eje_estatal", "type": "select_one", "select_from_list_name": "list_vias", "$kuid": make_kuid(), "label": ["Estado del eje vial estatal Piñas - Saracay (E585) y nodo estratégico 'La Y'"], "$qpath": "grp_vialidad/estado_eje_estatal", "$xpath": "grp_vialidad/estado_eje_estatal", "required": True, "$autoname": "estado_eje_estatal"},
    {"name": "estado_caminos_recintos", "type": "select_one", "select_from_list_name": "list_vias_vecinales", "$kuid": make_kuid(), "label": ["Estado general de los caminos vecinales hacia los recintos productivos"], "$qpath": "grp_vialidad/estado_caminos_recintos", "$xpath": "grp_vialidad/estado_caminos_recintos", "required": True, "$autoname": "estado_caminos_recintos"},
    {"name": "afectacion_crecidas", "type": "select_one", "select_from_list_name": "list_sino", "$kuid": make_kuid(), "label": ["¿El territorio sufre afectaciones recurrentes por crecidas del río Saracay o deslizamientos en invierno?"], "$qpath": "grp_vialidad/afectacion_crecidas", "$xpath": "grp_vialidad/afectacion_crecidas", "required": True, "$autoname": "afectacion_crecidas"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 4: Sistema Económico y Vocación Territorial
    {"name": "grp_productivo", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 4: Sistema Económico-Productivo y Comercio Estratégico"], "$qpath": "grp_productivo", "$xpath": "grp_productivo", "required": False, "$autoname": "grp_productivo"},
    {"name": "actividades_ingresos", "type": "select_multiple", "select_from_list_name": "list_actividades", "$kuid": make_kuid(), "label": ["Principales rubros y cadenas productivas motor de la economía parroquial (Selección múltiple)"], "$qpath": "grp_productivo/actividades_ingresos", "$xpath": "grp_productivo/actividades_ingresos", "required": True, "$autoname": "actividades_ingresos"},
    {"name": "potencial_comercial_la_y", "type": "select_one", "select_from_list_name": "list_nivel", "$kuid": make_kuid(), "label": ["Potencial comercial, turístico y gastronómico del nodo vial 'La Y' de Saracay"], "$qpath": "grp_productivo/potencial_comercial_la_y", "$xpath": "grp_productivo/potencial_comercial_la_y", "required": True, "$autoname": "potencial_comercial_la_y"},
    {"type": "end_group", "$kuid": make_kuid()},

    # Módulo 5: Prioridades de Inversión y Articulación
    {"name": "grp_prioridades", "type": "begin_group", "$kuid": make_kuid(), "label": ["Módulo 5: Prioridades de Inversión Pública y Proyectos"], "$qpath": "grp_prioridades", "$xpath": "grp_prioridades", "required": False, "$autoname": "grp_prioridades"},
    {"name": "prioridad_1_obra", "type": "select_one", "select_from_list_name": "list_prioridades", "$kuid": make_kuid(), "label": ["PRIORIDAD #1: Proyecto u obra pública más urgente para gestión o financiamiento"], "$qpath": "grp_prioridades/prioridad_1_obra", "$xpath": "grp_prioridades/prioridad_1_obra", "required": True, "$autoname": "prioridad_1_obra"},
    {"name": "prioridad_2_obra", "type": "select_one", "select_from_list_name": "list_prioridades", "$kuid": make_kuid(), "label": ["PRIORIDAD #2: Segunda obra pública prioritaria para Saracay"], "$qpath": "grp_prioridades/prioridad_2_obra", "$xpath": "grp_prioridades/prioridad_2_obra", "required": True, "$autoname": "prioridad_2_obra"},
    {"name": "obras_en_ejecucion", "type": "text", "$kuid": make_kuid(), "label": ["Obras y proyectos públicos actualmente en ejecución o articulados con GADM Piñas o Prefectura"], "$qpath": "grp_prioridades/obras_en_ejecucion", "$xpath": "grp_prioridades/obras_en_ejecucion", "required": False, "$autoname": "obras_en_ejecucion"},
    {"name": "criterio_proyecto_ptar_unl", "type": "text", "$kuid": make_kuid(), "label": ["Criterio institucional sobre la propuesta técnica UNL (Alcantarillado Sanitario y PTAR Saracay)"], "hint": ["Viabilidad, terreno disponible o predisposición del GAD"], "$qpath": "grp_prioridades/criterio_proyecto_ptar_unl", "$xpath": "grp_prioridades/criterio_proyecto_ptar_unl", "required": False, "$autoname": "criterio_proyecto_ptar_unl"},
    {"name": "foto_evidencia", "type": "image", "$kuid": make_kuid(), "label": ["Fotografía de respaldo de la visita institucional / Sede GAD"], "$qpath": "grp_prioridades/foto_evidencia", "$xpath": "grp_prioridades/foto_evidencia", "required": False, "$autoname": "foto_evidencia"},
    {"name": "nota_cierre", "type": "note", "$kuid": make_kuid(), "label": ["Agradecimiento: Muchas gracias al Sr. Jorge Homero Ochoa Sánchez, Presidente del GAD Parroquial de Saracay, por su valiosa colaboración con la Universidad Nacional de Loja para la formulación del proyecto."], "$qpath": "grp_prioridades/nota_cierre", "$xpath": "grp_prioridades/nota_cierre", "required": False, "$autoname": "nota_cierre"},
    {"type": "end_group", "$kuid": make_kuid()}
]

choices_raw = [
    # list_estado_pdot
    {"list_name": "list_estado_pdot", "name": "vigente_2023_2027", "label": ["Vigente y aprobado (PDOT Saracay 2023-2027)"], "$kuid": make_kuid(), "$autovalue": "vigente_2023_2027"},
    {"list_name": "list_estado_pdot", "name": "en_actualizacion", "label": ["En proceso formal de actualización y armonización"], "$kuid": make_kuid(), "$autovalue": "en_actualizacion"},
    {"list_name": "list_estado_pdot", "name": "desactualizado", "label": ["Desactualizado"], "$kuid": make_kuid(), "$autovalue": "desactualizado"},

    # list_calidad_agua
    {"list_name": "list_calidad_agua", "name": "buena", "label": ["Buena (tratada / apta para consumo con red matriz)"], "$kuid": make_kuid(), "$autovalue": "buena"},
    {"list_name": "list_calidad_agua", "name": "regular_entubada", "label": ["Regular (agua entubada sin cloración constante y turbiedad en invierno)"], "$kuid": make_kuid(), "$autovalue": "regular_entubada"},
    {"list_name": "list_calidad_agua", "name": "vertiente_quebrada", "label": ["Vertiente / Quebrada sin tratamiento en sectores periféricos"], "$kuid": make_kuid(), "$autovalue": "vertiente_quebrada"},

    # list_continuidad
    {"list_name": "list_continuidad", "name": "continua_24h", "label": ["Continua las 24 horas del día"], "$kuid": make_kuid(), "$autovalue": "continua_24h"},
    {"list_name": "list_continuidad", "name": "parcial_horas", "label": ["Parcial (ciertas horas al día / racionamiento estacional)"], "$kuid": make_kuid(), "$autovalue": "parcial_horas"},
    {"list_name": "list_continuidad", "name": "cortes_frecuentes", "label": ["Intermitente con cortes frecuentes en invierno/verano"], "$kuid": make_kuid(), "$autovalue": "cortes_frecuentes"},

    # list_saneamiento
    {"list_name": "list_saneamiento", "name": "red_parcial_sin_ptar", "label": ["Red de alcantarillado combinada y parcial en cabecera SIN PTAR (descarga cruda)"], "$kuid": make_kuid(), "$autovalue": "red_parcial_sin_ptar"},
    {"list_name": "list_saneamiento", "name": "predominio_pozos_letrinas", "label": ["Predominio casi total de pozos sépticos y letrinas (recintos y periferia)"], "$kuid": make_kuid(), "$autovalue": "predominio_pozos_letrinas"},
    {"list_name": "list_saneamiento", "name": "sistema_completo_ptar", "label": ["Sistema completo con Planta de Tratamiento operativa"], "$kuid": make_kuid(), "$autovalue": "sistema_completo_ptar"},

    # list_sino
    {"list_name": "list_sino", "name": "si", "label": ["Sí"], "$kuid": make_kuid(), "$autovalue": "si"},
    {"list_name": "list_sino", "name": "no", "label": ["No"], "$kuid": make_kuid(), "$autovalue": "no"},

    # list_vias
    {"list_name": "list_vias", "name": "asfaltada_buena", "label": ["Asfaltada en buen estado (Eje principal estatal E585)"], "$kuid": make_kuid(), "$autovalue": "asfaltada_buena"},
    {"list_name": "list_vias", "name": "regular_bacheo", "label": ["Regular con baches frecuentes (requiere mantenimiento vial)"], "$kuid": make_kuid(), "$autovalue": "regular_bacheo"},
    {"list_name": "list_vias", "name": "critica_invierno", "label": ["Crítica por fallas geológicas o pérdida de calzada"], "$kuid": make_kuid(), "$autovalue": "critica_invierno"},

    # list_vias_vecinales
    {"list_name": "list_vias_vecinales", "name": "lastrada_buena", "label": ["Lastrada con mantenimiento continuo del GADPR y Prefectura"], "$kuid": make_kuid(), "$autovalue": "lastrada_buena"},
    {"list_name": "list_vias_vecinales", "name": "regular_baches", "label": ["Regular (afirmada con baches, transitable con precaución)"], "$kuid": make_kuid(), "$autovalue": "regular_baches"},
    {"list_name": "list_vias_vecinales", "name": "mala_intransitable_invierno", "label": ["Mala / Intransitable en temporada invernal"], "$kuid": make_kuid(), "$autovalue": "mala_intransitable_invierno"},

    # list_actividades
    {"list_name": "list_actividades", "name": "cana_panela", "label": ["Cultivo de caña de azúcar y molienda de panela (58% PEA)"], "$kuid": make_kuid(), "$autovalue": "cana_panela"},
    {"list_name": "list_actividades", "name": "maiz_granos", "label": ["Producción de maíz duro y granos"], "$kuid": make_kuid(), "$autovalue": "maiz_granos"},
    {"list_name": "list_actividades", "name": "platano_cacao", "label": ["Plátano y cacao fino de aroma"], "$kuid": make_kuid(), "$autovalue": "platano_cacao"},
    {"list_name": "list_actividades", "name": "ganaderia_carne_leche", "label": ["Ganadería bovina de carne y leche (7% PEA)"], "$kuid": make_kuid(), "$autovalue": "ganaderia_carne_leche"},
    {"list_name": "list_actividades", "name": "comercio_gastronomia_la_y", "label": ["Comercio gastronómico, transporte y paradores en La Y (32% PEA)"], "$kuid": make_kuid(), "$autovalue": "comercio_gastronomia_la_y"},
    {"list_name": "list_actividades", "name": "citricos_frutales", "label": ["Cítricos (naranja, mandarina, limón) y frutales menores"], "$kuid": make_kuid(), "$autovalue": "citricos_frutales"},

    # list_nivel
    {"list_name": "list_nivel", "name": "alto", "label": ["Alto"], "$kuid": make_kuid(), "$autovalue": "alto"},
    {"list_name": "list_nivel", "name": "medio", "label": ["Medio"], "$kuid": make_kuid(), "$autovalue": "medio"},
    {"list_name": "list_nivel", "name": "bajo", "label": ["Bajo"], "$kuid": make_kuid(), "$autovalue": "bajo"},

    # list_prioridades
    {"list_name": "list_prioridades", "name": "alcantarillado_ptar", "label": ["Alcantarillado sanitario y Planta de Tratamiento de Aguas Residuales (PTAR)"], "$kuid": make_kuid(), "$autovalue": "alcantarillado_ptar"},
    {"list_name": "list_prioridades", "name": "agua_potable_optimizacion", "label": ["Optimización y ampliación de reservorios de agua potable"], "$kuid": make_kuid(), "$autovalue": "agua_potable_optimizacion"},
    {"list_name": "list_prioridades", "name": "vias_recintos", "label": ["Asfaltado y mejoramiento vial a recintos (Platanillos, Panupali, Naranjos)"], "$kuid": make_kuid(), "$autovalue": "vias_recintos"},
    {"list_name": "list_prioridades", "name": "ordenamiento_la_y", "label": ["Ordenamiento urbano, drenaje y parador turístico en La Y"], "$kuid": make_kuid(), "$autovalue": "ordenamiento_la_y"},
    {"list_name": "list_prioridades", "name": "salud_equipamiento", "label": ["Ampliación y equipamiento del Centro de Salud Rural"], "$kuid": make_kuid(), "$autovalue": "salud_equipamiento"},
    {"list_name": "list_prioridades", "name": "defensas_rio", "label": ["Muros de contención y defensas ribereñas en el río Saracay"], "$kuid": make_kuid(), "$autovalue": "defensas_rio"}
]

payload_asset = {
    "name": "Guía de Entrevista Institucional - Presidente GAD Parroquial Saracay (UNL)",
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

print("1. Creando Formulario Institucional para Presidente del GAD...")
r_create = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=payload_asset)
print("Create Status:", r_create.status_code)

if r_create.status_code in [200, 201]:
    uid = r_create.json().get("uid")
    print("UID del Formulario:", uid)

    print("2. Desplegando versión oficial en KoboToolbox...")
    r_dep = requests.post(
        f"{BASE_URL}/api/v2/assets/{uid}/deployment/",
        headers=headers_dep,
        data={"active": "true"}
    )
    print("Deploy Status:", r_dep.status_code)

    if r_dep.status_code in [200, 201]:
        r_final = requests.get(f"{BASE_URL}/api/v2/assets/{uid}/", headers=headers)
        links = r_final.json().get("deployment__links", {})
        print("\n" + "="*75)
        print("¡FORMULARIO PARA EL PRESIDENTE DEL GAD SARACAY DESPLEGADO EXITOSAMENTE!")
        print(f"UID del Formulario: {uid}")
        print(f"URL Web Enketo (Online): {links.get('url')}")
        print(f"URL Envío Único:         {links.get('single_url')}")
        print(f"URL Offline (Kobo App):   {links.get('offline_url')}")
        print("="*75)
    else:
        print("Error en Deployment:", r_dep.text[:400])
else:
    print("Error al crear:", r_create.text[:400])
