import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# Estructura de Entrevista Institucional para Autoridad Local (Presidente del GAD Parroquial)
survey = [
    # Metadatos automáticos
    {"name": "start", "type": "start"},
    {"name": "end", "type": "end"},
    {"name": "today", "type": "today"},
    
    # Módulo 0: Metadatos y Control Institucional
    {"name": "grp_control", "type": "begin_group", "label": "Módulo 0: Metadatos y Control de la Entrevista Institucional"},
    {"name": "nota_protocolo", "type": "note", "label": "Entrevista de Diagnóstico Territorial y Línea Base de Inversión Pública dirigida a la Autoridad Parroquial de Saracay (Sr. Jorge Homero Ochoa Sánchez - Presidente GADPR Saracay 2023-2027)."},
    {"name": "encuestador", "type": "text", "label": "Investigador / Entrevistador UNL", "required": True},
    {"name": "fecha_entrevista", "type": "date", "label": "Fecha de la entrevista institucional", "required": True},
    {"name": "gps_punto", "type": "geopoint", "label": "Ubicación geográfica GPS (Sede GAD Parroquial Saracay)"},
    {"name": "grp_control", "type": "end_group"},

    # Módulo 1: Marco de Planificación y Gestión Territorial
    {"name": "grp_planificacion", "type": "begin_group", "label": "Módulo 1: Marco de Planificación y Delimitación Territorial"},
    {"name": "pdot_estado", "type": "select_one", "select_from_list_name": "list_estado_pdot", "label": "Estado de actualización del Plan de Desarrollo y Ordenamiento Territorial (PDOT)", "required": True},
    {"name": "pdot_periodo", "type": "text", "label": "Vigencia del PDOT e instrumentos articulados con el GAD Municipal de Piñas", "required": False},
    {"name": "recintos_prioritarios", "type": "text", "label": "Recintos o comunidades que demandan mayor atención institucional emergente", "required": True},
    {"name": "grp_planificacion", "type": "end_group"},

    # Módulo 2: Saneamiento Básico y Agua Potable
    {"name": "grp_servicios", "type": "begin_group", "label": "Módulo 2: Diagnóstico Institucional de Agua, Saneamiento y Residuos"},
    {"name": "estado_cobertura_agua", "type": "select_one", "select_from_list_name": "list_nivel_servicio", "label": "Situación general de la cobertura y calidad del agua en la cabecera y recintos", "required": True},
    {"name": "continuidad_agua_parroquia", "type": "select_one", "select_from_list_name": "list_continuidad", "label": "Continuidad del suministro de agua en el casco central", "required": True},
    {"name": "situacion_alcantarillado_ptar", "type": "select_one", "select_from_list_name": "list_alcantarillado_ptar", "label": "Situación del sistema de alcantarillado sanitario y PTAR en Saracay", "required": True},
    {"name": "descargas_rio_saracay", "type": "select_one", "select_from_list_name": "list_sino", "label": "¿Existen descargas crudas de aguas servidas directamente al río Saracay o afluentes?", "required": True},
    {"name": "coordinacion_epaa_pinas", "type": "text", "label": "Mecanismos y convenios con EPAA-Piñas o Juntas Administradoras para operación del servicio"},
    {"name": "grp_servicios", "type": "end_group"},

    # Módulo 3: Vialidad, Conectividad y Riesgos Territoriales
    {"name": "grp_vialidad", "type": "begin_group", "label": "Módulo 3: Conectividad Vial, Articulación Regional y Riesgos"},
    {"name": "estado_eje_estatal", "type": "select_one", "select_from_list_name": "list_vias", "label": "Estado del eje vial estatal Piñas - Saracay (E585) y nodo estratégico 'La Y'", "required": True},
    {"name": "estado_caminos_vecinales", "type": "select_one", "select_from_list_name": "list_vias_vecinales", "label": "Estado de la red vial terciaria y caminos vecinales a recintos productivos", "required": True},
    {"name": "amenazas_climaticas", "type": "select_multiple", "select_from_list_name": "list_amenazas", "label": "Amenazas naturales recurrentes que afectan la infraestructura y producción local", "required": True},
    {"name": "capacidad_respuesta_riesgos", "type": "select_one", "select_from_list_name": "list_nivel", "label": "Capacidad operativa y planes de contingencia ante crecidas del río o deslaves", "required": True},
    {"name": "grp_vialidad", "type": "end_group"},

    # Módulo 4: Dinamización Económica y Vocación Territorial
    {"name": "grp_productivo", "type": "begin_group", "label": "Módulo 4: Componente Económico-Productivo y Comercio Estratégico"},
    {"name": "cadenas_productivas_clave", "type": "select_multiple", "select_from_list_name": "list_actividades", "label": "Cadenas productivas agropecuarias prioritarias para el fomento parroquial", "required": True},
    {"name": "estrategia_nodo_la_y", "type": "text", "label": "Visión de desarrollo comercial y turístico para el parador vial de 'La Y' de Saracay"},
    {"name": "apoyo_asociatividad_productiva", "type": "select_one", "select_from_list_name": "list_sino", "label": "¿Existen asociaciones agropecuarias o gremiales que reciban asistencia técnica del GAD?", "required": True},
    {"name": "grp_productivo", "type": "end_group"},

    # Módulo 5: Prioridades de Inversión y Articulación Multinivel
    {"name": "grp_prioridades", "type": "begin_group", "label": "Módulo 5: Prioridades de Inversión Pública y Proyectos en Marcha"},
    {"name": "prioridad_1_inversion_gad", "type": "select_one", "select_from_list_name": "list_prioridades", "label": "PRIORIDAD #1: Proyecto u obra pública más urgente para financiamiento/gestión", "required": True},
    {"name": "prioridad_2_inversion_gad", "type": "select_one", "select_from_list_name": "list_prioridades", "label": "PRIORIDAD #2: Segunda obra prioritaria para Saracay", "required": True},
    {"name": "cartera_proyectos_vigentes", "type": "text", "label": "Principales proyectos y convenios actualmente en ejecución o por contratar (GADPR, Alcaldía, Prefectura)"},
    {"name": "viabilidad_proyecto_unl", "type": "text", "label": "Criterio del GAD respecto al Proyecto propuesto por UNL (Saneamiento y PTAR Saracay)"},
    {"name": "foto_acta_visita", "type": "image", "label": "Fotografía de respaldo de la reunión institucional / Sede GAD"},
    {"name": "nota_cierre", "type": "note", "label": "Agradecimiento institucional: Agradecemos sinceramente al Sr. Jorge Homero Ochoa Sánchez, Presidente del GADPR Saracay, por su valiosa colaboración con la Universidad Nacional de Loja para la formulación del proyecto de inversión."},
    {"name": "grp_prioridades", "type": "end_group"}
]

# Choices estandarizadas
choices = [
    # list_estado_pdot
    {"list_name": "list_estado_pdot", "name": "vigente_aprobado", "label": "Vigente y aprobado (Periodo 2023-2027)"},
    {"list_name": "list_estado_pdot", "name": "en_actualizacion", "label": "En proceso de actualización formal"},
    {"list_name": "list_estado_pdot", "name": "desactualizado", "label": "Desactualizado / Por iniciar"},

    # list_nivel_servicio
    {"list_name": "list_nivel_servicio", "name": "bueno_potable", "label": "Satisfactorio (cobertura adecuada con tratamiento continuo)"},
    {"list_name": "list_nivel_servicio", "name": "regular_intermitente", "label": "Regular (cobertura parcial o problemas estacionales de turbiedad)"},
    {"list_name": "list_nivel_servicio", "name": "critico_deficitario", "label": "Crítico (déficit severo en recintos y red deteriorada)"},

    # list_continuidad
    {"list_name": "list_continuidad", "name": "continua_24h", "label": "Continua (24 horas)"},
    {"list_name": "list_continuidad", "name": "parcial_horas", "label": "Parcial (entre 12 y 18 horas diarias)"},
    {"list_name": "list_continuidad", "name": "intermitente_turnos", "label": "Intermitente (pocas horas al día o por turnos)"},

    # list_alcantarillado_ptar
    {"list_name": "list_alcantarillado_ptar", "name": "cobertura_parcial_sin_ptar", "label": "Red combinada parcial en cabecera SIN Planta de Tratamiento (Descarga cruda)"},
    {"list_name": "list_alcantarillado_ptar", "name": "inexistente_pozos", "label": "Inexistente en recintos (predominio total de pozos sépticos y letrinas)"},
    {"list_name": "list_alcantarillado_ptar", "name": "ptar_operativa", "label": "Sistema completo con PTAR operativa y certificada"},

    # list_sino
    {"list_name": "list_sino", "name": "si", "label": "Sí"},
    {"list_name": "list_sino", "name": "no", "label": "No"},

    # list_vias
    {"list_name": "list_vias", "name": "muy_bueno", "label": "Bueno (asfalto en condiciones transitables)"},
    {"list_name": "list_vias", "name": "regular_bacheo", "label": "Regular (requiere bacheo tecnificado y mantenimiento continuo)"},
    {"list_name": "list_vias", "name": "critico_puntos", "label": "Crítico (puntos con fallas geológicas o pérdida de calzada)"},

    # list_vias_vecinales
    {"list_name": "list_vias_vecinales", "name": "lastrado_bueno", "label": "Lastrado en buen estado con mantenimiento regular"},
    {"list_name": "list_vias_vecinales", "name": "regular_transitable", "label": "Regular (transitable solo en verano; difícil en invierno)"},
    {"list_name": "list_vias_vecinales", "name": "intransitable_invierno", "label": "Malo / Frecuentemente incomunicado por lluvias"},

    # list_amenazas
    {"list_name": "list_amenazas", "name": "crecidas_rio_saracay", "label": "Crecidas e inundaciones ribereñas del río Saracay o afluentes"},
    {"list_name": "list_amenazas", "name": "deslizamientos_taludes", "label": "Deslizamientos y pérdida de calzada en vías"},
    {"list_name": "list_amenazas", "name": "estiaje_sequia", "label": "Déficit hídrico en temporadas de estiaje prolongado"},
    {"list_name": "list_amenazas", "name": "contaminacion_vertidos", "label": "Contaminación hídrica por aguas servidas o lixiviados"},

    # list_nivel
    {"list_name": "list_nivel", "name": "alto", "label": "Alto"},
    {"list_name": "list_nivel", "name": "medio", "label": "Medio"},
    {"list_name": "list_nivel", "name": "bajo", "label": "Bajo / Carente de equipamiento"},

    # list_actividades
    {"list_name": "list_actividades", "name": "cana_panela", "label": "Caña de azúcar y molienda de panela artesanal"},
    {"list_name": "list_actividades", "name": "maiz_granos", "label": "Producción de maíz duro y granos"},
    {"list_name": "list_actividades", "name": "platano_cacao", "label": "Cacao fino de aroma y plátano"},
    {"list_name": "list_actividades", "name": "ganaderia_carne_leche", "label": "Ganadería bovina de doble propósito"},
    {"list_name": "list_actividades", "name": "citricos_frutales", "label": "Cítricos (naranja, mandarina, limón) y frutales"},
    {"list_name": "list_actividades", "name": "comercio_gastronomia_la_y", "label": "Sector comercial, gastronómico y servicios en 'La Y'"},

    # list_prioridades
    {"list_name": "list_prioridades", "name": "alcantarillado_ptar", "label": "Construcción / Optimización de Alcantarillado Sanitario y PTAR"},
    {"list_name": "list_prioridades", "name": "agua_potable_reservorios", "label": "Ampliación del sistema de Agua Potable y Reservorios"},
    {"list_name": "list_prioridades", "name": "asfaltado_vias_recintos", "label": "Asfaltado y mejoramiento vial a recintos (Platanillos, Panupali, Naranjos)"},
    {"list_name": "list_prioridades", "name": "ordenamiento_parador_la_y", "label": "Ordenamiento urbano, drenaje y Parador Turístico 'La Y'"},
    {"list_name": "list_prioridades", "name": "defensas_riberenas", "label": "Muros de escolleras y protección ribereña del río Saracay"},
    {"list_name": "list_prioridades", "name": "salud_equipamiento", "label": "Ampliación y equipamiento del Centro de Salud Rural"}
]

# Configurar el asset para KoboToolbox
payload_asset = {
    "name": "Entrevista de Diagnóstico Territorial - Autoridad Parroquial Saracay (UNL)",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": survey,
        "choices": choices,
        "settings": {
            "title": "Entrevista a la Autoridad Parroquial - Saracay (UNL)",
            "id_string": "saracay_entrevista_autoridad_unl_2026"
        }
    })
}

print("1. Creando Formulario en KoboToolbox para la Autoridad Parroquial...")
r_create = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=payload_asset)
print("Create Status:", r_create.status_code)

if r_create.status_code in [200, 201]:
    asset_data = r_create.json()
    uid = asset_data.get("uid")
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
        final_info = r_final.json()
        links = final_info.get("deployment__links", {})
        print("\n" + "="*75)
        print("¡ENTREVISTA OFICIAL A LA AUTORIDAD PARROQUIAL DESPLEGADA CON ÉXITO!")
        print(f"UID: {uid}")
        print(f"Enlace Web Enketo (Online): {links.get('url')}")
        print(f"Enlace de Envío Único:      {links.get('single_url')}")
        print(f"Enlace Offline / Kobo App:  {links.get('offline_url')}")
        print("="*75)
    else:
        print("Error en Deployment:", r_dep.text[:400])
else:
    print("Error al crear Asset:", r_create.text[:400])
