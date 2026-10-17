import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# Estructura de Entrevista Institucional - Proyecto Construcción de Puente en Torata
survey = [
    # Metadatos automáticos
    {"name": "start", "type": "start"},
    {"name": "end", "type": "end"},
    {"name": "today", "type": "today"},
    
    # Módulo 0: Metadatos y Control Institucional
    {"name": "grp_control", "type": "begin_group", "label": "Módulo 0: Metadatos y Control de la Entrevista (Torata - Puente)"},
    {"name": "nota_protocolo", "type": "note", "label": "Entrevista de Diagnóstico Territorial y Línea Base de Inversión Pública: Proyecto de Construcción / Reposición de Puente en la Parroquia Rural Torata, Cantón Santa Rosa, El Oro (UNL)."},
    {"name": "encuestador", "type": "text", "label": "Investigador / Entrevistador UNL", "required": True},
    {"name": "nombre_entrevistado", "type": "text", "label": "Nombre del entrevistado/a o autoridad local", "required": True},
    {"name": "cargo_entrevistado", "type": "text", "label": "Cargo / Representación comunitaria", "required": True},
    {"name": "fecha_entrevista", "type": "date", "label": "Fecha de la entrevista", "required": True},
    {"name": "gps_punto", "type": "geopoint", "label": "Ubicación geográfica GPS (Lugar de la entrevista o emplazamiento del puente)"},
    {"name": "grp_control", "type": "end_group"},

    # Módulo 1: Marco de Planificación y Delimitación Territorial
    {"name": "grp_planificacion", "type": "begin_group", "label": "Módulo 1: Planificación Territorial y Articulación Institucional"},
    {"name": "pdot_estado", "type": "select_one", "select_from_list_name": "list_estado_pdot", "label": "Estado de actualización del PDOT de Torata", "required": True},
    {"name": "articulacion_gobiernos", "type": "text", "label": "Nivel de coordinación entre GAD Parroquial Torata, GAD Municipal Santa Rosa y Prefectura de El Oro"},
    {"name": "recintos_beneficiarios", "type": "text", "label": "Comunidades, recintos o barrios directamente beneficiados por el paso", "required": True},
    {"name": "grp_planificacion", "type": "end_group"},

    # Módulo 2: Diagnóstico Específico del Cruce y Puente
    {"name": "grp_diagnostico_puente", "type": "begin_group", "label": "Módulo 2: Diagnóstico Específico del Puente y Conectividad Vial"},
    {"name": "estado_cruce_actual", "type": "select_one", "select_from_list_name": "list_estado_cruce", "label": "Situación actual de la infraestructura del paso / cruce del río", "required": True},
    {"name": "frecuencia_incomunicacion", "type": "select_one", "select_from_list_name": "list_frecuencia_aislamiento", "label": "¿Con qué frecuencia e intensidad queda incomunicada la población durante la época de lluvias?", "required": True},
    {"name": "dias_interrupcion_ano", "type": "integer", "label": "Número estimado de días al año en que el cruce está totalmente inhabilitado por el río"},
    {"name": "tipo_transporte_requerido", "type": "select_multiple", "select_from_list_name": "list_transporte", "label": "Tipo de tráfico y usuarios que demandan el cruce", "required": True},
    {"name": "longitud_aproximada_luz", "type": "text", "label": "Ancho del cauce / Luz estimada necesaria para el puente (metros)"},
    {"name": "grp_diagnostico_puente", "type": "end_group"},

    # Módulo 3: Impacto Socioeconómico y Cadenas Productivas
    {"name": "grp_impacto_socioeconomico", "type": "begin_group", "label": "Módulo 3: Impacto en la Producción y Servicios Básicos"},
    {"name": "cadenas_productivas_afectadas", "type": "select_multiple", "select_from_list_name": "list_cultivos_torata", "label": "Cadenas agropecuarias afectadas por la falta o mal estado del puente", "required": True},
    {"name": "afectacion_cosechas", "type": "select_one", "select_from_list_name": "list_afectacion_economica", "label": "¿Cuál es la principal afectación económica para los agricultores y ganaderos?", "required": True},
    {"name": "sobrecosto_flete_estimado", "type": "decimal", "label": "Sobrecosto estimado por bulto/quintal/trasbordo manual cuando no hay paso ($ USD)"},
    {"name": "afectacion_educacion_salud", "type": "select_multiple", "select_from_list_name": "list_servicios_afectados", "label": "Impacto en servicios sociales (educación escolar, traslados médicos de emergencia)", "required": True},
    {"name": "grp_impacto_socioeconomico", "type": "end_group"},

    # Módulo 4: Análisis de Riesgos y Gestión Institucional
    {"name": "grp_riesgos_gestion", "type": "begin_group", "label": "Módulo 4: Riesgos, Seguridad y Viabilidad de la Inversión"},
    {"name": "antecedentes_accidentes", "type": "select_one", "select_from_list_name": "list_sino", "label": "¿Se han registrado accidentes o emergencias graves por intentar cruzar el río crecido?", "required": True},
    {"name": "descripcion_accidentes", "type": "text", "label": "Detalle de antecedentes de riesgo o eventos críticos registrados"},
    {"name": "estado_estudios_previos", "type": "select_one", "select_from_list_name": "list_estudios", "label": "Estado de estudios técnicos previos por parte de la Prefectura o Municipio", "required": True},
    {"name": "nivel_prioridad_proyecto", "type": "select_one", "select_from_list_name": "list_prioridad", "label": "Nivel de prioridad comunitaria para la ejecución de este puente", "required": True},
    {"name": "foto_cruce_rio", "type": "image", "label": "Fotografía del cauce del río / paso actual o puente colapsado"},
    {"name": "foto_entrevista", "type": "image", "label": "Fotografía con el entrevistado/a o acta de respaldo"},
    {"name": "nota_cierre", "type": "note", "label": "Agradecimiento institucional: Gracias por participar en la formulación técnica de proyectos de inversión de la Universidad Nacional de Loja para la Parroquia Torata."},
    {"name": "grp_riesgos_gestion", "type": "end_group"}
]

choices = [
    # list_estado_pdot
    {"list_name": "list_estado_pdot", "name": "vigente_aprobado", "label": "Vigente y aprobado (2023-2027)"},
    {"list_name": "list_estado_pdot", "name": "en_actualizacion", "label": "En proceso de actualización formal"},
    {"list_name": "list_estado_pdot", "name": "desactualizado", "label": "Desactualizado / Sin vigencia"},

    # list_estado_cruce
    {"list_name": "list_estado_cruce", "name": "inexistente_vado", "label": "Inexistente (cruce por badén/vado natural en el lecho del río)"},
    {"list_name": "list_estado_cruce", "name": "colapsado_destruido", "label": "Puente colapsado o destruido por crecidas invernales anteriores"},
    {"list_name": "list_estado_cruce", "name": "provisional_madera", "label": "Puente provisional de madera/caña con alto riesgo de caída"},
    {"list_name": "list_estado_cruce", "name": "antiguo_critico", "label": "Estructura antigua en estado crítico (deterioro severo o socavación)"},

    # list_frecuencia_aislamiento
    {"list_name": "list_frecuencia_aislamiento", "name": "cada_lluvia_fuerte", "label": "Con cada lluvia fuerte / crecida repentina del río"},
    {"list_name": "list_frecuencia_aislamiento", "name": "temporada_invernal_entera", "label": "Intermitente durante toda la temporada invernal (varios meses)"},
    {"list_name": "list_frecuencia_aislamiento", "name": "aislamiento_permanente", "label": "Paso permanentemente riesgoso y precario todo el año"},

    # list_transporte
    {"list_name": "list_transporte", "name": "peatonal_acemilas", "label": "Peatones y acémilas (caballos/mulas)"},
    {"list_name": "list_transporte", "name": "motos_camionetas", "label": "Motocicletas y camionetas livianas de familias rurales"},
    {"list_name": "list_transporte", "name": "camiones_carga_media", "label": "Camiones medianos para sacar cosechas agrícolas"},
    {"list_name": "list_transporte", "name": "transporte_pesado", "label": "Camiones pesados de ganado o material de construcción"},
    {"list_name": "list_transporte", "name": "transporte_escolar", "label": "Buses o furgonetas de transporte escolar"},

    # list_cultivos_torata
    {"list_name": "list_cultivos_torata", "name": "cacao", "label": "Cacao nacional y fino de aroma"},
    {"list_name": "list_cultivos_torata", "name": "platano_guineo", "label": "Plátano, guineo y frutas tropicales"},
    {"list_name": "list_cultivos_torata", "name": "maiz_granos", "label": "Maíz duro y granos"},
    {"list_name": "list_cultivos_torata", "name": "ganaderia_leche_carne", "label": "Ganadería bovina (carne y leche)"},
    {"list_name": "list_cultivos_torata", "name": "citricos", "label": "Cítricos (naranja, mandarina, limón)"},
    {"list_name": "list_cultivos_torata", "name": "cana_panela", "label": "Caña de azúcar y molienda"},

    # list_afectacion_economica
    {"list_name": "list_afectacion_economica", "name": "perdida_total_cosecha", "label": "Pérdida o pudrición de cosechas en finca por falta de salida"},
    {"list_name": "list_afectacion_economica", "name": "castigo_precios_intermediarios", "label": "Venta a intermediarios a precios castigados de remate"},
    {"list_name": "list_afectacion_economica", "name": "sobrecosto_trasbordo", "label": "Pago de fletes dobles o trasbordos manuales excesivos"},

    # list_servicios_afectados
    {"list_name": "list_servicios_afectados", "name": "estudiantes_pierden_clases", "label": "Estudiantes no pueden asistir a clases por crecida del río"},
    {"list_name": "list_servicios_afectados", "name": "cruce_arriesgado_estudiantes", "label": "Niños y jóvenes cruzan el río arriesgando su vida"},
    {"list_name": "list_servicios_afectados", "name": "ambulancias_no_entran", "label": "Imposibilidad de ingreso de ambulancias o atención médica de emergencia"},
    {"list_name": "list_servicios_afectados", "name": "traslado_enfermos_hamaca", "label": "Necesidad de cargar enfermos y ancianos a pie o en hamacas"},

    # list_sino
    {"list_name": "list_sino", "name": "si", "label": "Sí"},
    {"list_name": "list_sino", "name": "no", "label": "No"},

    # list_estudios
    {"list_name": "list_estudios", "name": "sin_estudios", "label": "Sin estudios técnicos existentes (requiere formulación integral)"},
    {"list_name": "list_estudios", "name": "estudios_preliminares", "label": "Cuenta con inspección o topografía preliminar sin financiamiento"},
    {"list_name": "list_estudios", "name": "estudios_completos_sin_fondos", "label": "Estudios definitivos listos a la espera de financiamiento público"},

    # list_prioridad
    {"list_name": "list_prioridad", "name": "maxima_urgente", "label": "Prioridad Máxima / Emergente (Urgencia de vida y productividad)"},
    {"list_name": "list_prioridad", "name": "alta", "label": "Prioridad Alta"},
    {"list_name": "list_prioridad", "name": "media", "label": "Prioridad Media"}
]

payload_asset = {
    "name": "Entrevista de Diagnóstico Territorial - Proyecto Puente Torata (UNL)",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": survey,
        "choices": choices,
        "settings": {
            "title": "Entrevista Diagnóstico Territorial - Proyecto Puente Torata (UNL)",
            "id_string": "torata_entrevista_puente_unl_2026"
        }
    })
}

print("1. Creando Formulario en KoboToolbox para Entrevista Torata (Puente)...")
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
        print("¡FORMULARIO KOBOTOOLBOX DE ENTREVISTA TORATA DESPLEGADO CON ÉXITO!")
        print(f"UID: {uid}")
        print(f"Enlace Web Enketo (Online): {links.get('url')}")
        print(f"Enlace de Envío Único:      {links.get('single_url')}")
        print(f"Enlace Offline / Kobo App:  {links.get('offline_url')}")
        print("="*75)
    else:
        print("Error en Deployment:", r_dep.text[:400])
else:
    print("Error al crear Asset:", r_create.text[:400])
