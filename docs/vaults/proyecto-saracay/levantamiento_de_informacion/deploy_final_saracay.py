import requests
import json

TOKEN = "f4dd70dfbc9497d25d834ec2fbeebfa132562b46"
BASE_URL = "https://kf.kobotoolbox.org"
headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
headers_dep = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}

# 1. Obtener la encuesta de Saracay que funcionó en test_no_relevant (UID: r2)
# Recreamos la encuesta completa con los 5 módulos organizados y relevantes compatibles
survey = [
    # Metadatos automáticos
    {"name": "start", "type": "start"},
    {"name": "end", "type": "end"},
    {"name": "today", "type": "today"},
    
    # Módulo 0
    {"name": "grp_control", "type": "begin_group", "label": "Módulo 0: Metadatos y Control de la Entrevista"},
    {"name": "encuestador", "type": "text", "label": "Nombre del Encuestador / Investigador UNL", "required": True},
    {"name": "fecha_entrevista", "type": "date", "label": "Fecha de la entrevista", "required": True},
    {"name": "gps_punto", "type": "geopoint", "label": "Ubicación geográfica GPS del punto de levantamiento"},
    {"name": "sector_saracay", "type": "select_one", "select_from_list_name": "list_sectores", "label": "Sector, Ciudadela o Recinto de Saracay (Piñas, El Oro)", "required": True},
    {"name": "sector_otro", "type": "text", "label": "Especifique el nombre del sector o recinto (si seleccionó 'Otro')", "relevant": "selected(${sector_saracay}, 'otro')"},
    {"name": "grp_control", "type": "end_group"},

    # Módulo 1
    {"name": "grp_informante", "type": "begin_group", "label": "Módulo 1: Perfil del Informante Clave"},
    {"name": "nombre_informante", "type": "text", "label": "Nombre completo del informante", "required": True},
    {"name": "rol_comunidad", "type": "select_one", "select_from_list_name": "list_roles", "label": "Cargo o función principal en Saracay", "required": True},
    {"name": "rol_otro", "type": "text", "label": "Especifique su cargo u ocupación (si seleccionó 'Otro')", "relevant": "selected(${rol_comunidad}, 'otro')"},
    {"name": "rango_edad", "type": "select_one", "select_from_list_name": "list_edad", "label": "Rango de edad del informante", "required": True},
    {"name": "tiempo_residencia", "type": "integer", "label": "¿Cuántos años reside en la Parroquia Saracay?", "required": True},
    {"name": "grp_informante", "type": "end_group"},

    # Módulo 2
    {"name": "grp_servicios", "type": "begin_group", "label": "Módulo 2: Diagnóstico de Agua, Saneamiento y Residuos"},
    {"name": "calidad_agua", "type": "select_one", "select_from_list_name": "list_calidad_agua", "label": "¿Cómo califica la calidad y servicio de agua de consumo en su sector?", "required": True},
    {"name": "continuidad_agua", "type": "select_one", "select_from_list_name": "list_continuidad", "label": "Continuidad del servicio de agua durante el día", "required": True},
    {"name": "sistema_saneamiento", "type": "select_one", "select_from_list_name": "list_saneamiento", "label": "Tipo de sistema para evacuación de aguas servidas / excretas en su vivienda", "required": True},
    {"name": "frecuencia_basura", "type": "select_one", "select_from_list_name": "list_recoleccion", "label": "Frecuencia de recolección de basura (GAD Municipal de Piñas)", "required": True},
    {"name": "problemas_saneamiento_obs", "type": "text", "label": "Principales deficiencias identificadas (Ej. turbiedad en invierno, cortes, vertidos sin PTAR al río Saracay)"},
    {"name": "grp_servicios", "type": "end_group"},

    # Módulo 3
    {"name": "grp_vialidad", "type": "begin_group", "label": "Módulo 3: Vialidad y Conectividad Territorial"},
    {"name": "estado_vias_acceso", "type": "select_one", "select_from_list_name": "list_vias", "label": "Estado de las vías y accesos hacia su sector o recinto", "required": True},
    {"name": "acceso_internet", "type": "select_one", "select_from_list_name": "list_internet", "label": "Acceso a conectividad de internet", "required": True},
    {"name": "afectacion_crecidas", "type": "select_one", "select_from_list_name": "list_sino", "label": "¿Su sector o cultivos sufren daños por deslizamientos o crecidas del río Saracay en invierno?", "required": True},
    {"name": "grp_vialidad", "type": "end_group"},

    # Módulo 4
    {"name": "grp_productivo", "type": "begin_group", "label": "Módulo 4: Sistema Económico y Productivo"},
    {"name": "actividades_ingresos", "type": "select_multiple", "select_from_list_name": "list_actividades", "label": "Principales actividades económicas generadoras de ingresos (Selección múltiple)", "required": True},
    {"name": "canal_comercializacion", "type": "select_one", "select_from_list_name": "list_comercializacion", "label": "Canal principal de venta de sus productos", "required": True},
    {"name": "percepcion_turismo_la_y", "type": "select_one", "select_from_list_name": "list_nivel", "label": "Potencial comercial y turístico del sector La Y de Saracay", "required": True},
    {"name": "grp_productivo", "type": "end_group"},

    # Módulo 5
    {"name": "grp_prioridades", "type": "begin_group", "label": "Módulo 5: Prioridades de Inversión Pública para Saracay"},
    {"name": "prioridad_1_obra", "type": "select_one", "select_from_list_name": "list_prioridades", "label": "PRIORIDAD #1: Proyecto u obra pública más urgente para la parroquia", "required": True},
    {"name": "prioridad_2_obra", "type": "select_one", "select_from_list_name": "list_prioridades", "label": "PRIORIDAD #2: Segunda obra prioritaria para Saracay", "required": True},
    {"name": "obras_en_ejecucion", "type": "text", "label": "Obras o proyectos públicos que conozca actualmente en ejecución en la parroquia"},
    {"name": "foto_evidencia", "type": "image", "label": "Fotografía de evidencia de la visita o infraestructura (Opcional)"},
    {"name": "nota_cierre", "type": "note", "label": "Muchas gracias por su colaboración con la Universidad Nacional de Loja y el diagnóstico territorial de la Parroquia Saracay (Piñas, El Oro)."},
    {"name": "grp_prioridades", "type": "end_group"}
]

# Choices
choices = [
    # list_sectores
    {"list_name": "list_sectores", "name": "cabecera_central", "label": "Cabecera Parroquial - Sector Central"},
    {"list_name": "list_sectores", "name": "la_y_saracay", "label": "Sector La Y de Saracay (Nodo vial E585 / E25)"},
    {"list_name": "list_sectores", "name": "el_bosque", "label": "Ciudadela El Bosque"},
    {"list_name": "list_sectores", "name": "el_tamarindo", "label": "Ciudadela El Tamarindo"},
    {"list_name": "list_sectores", "name": "la_inmaculada", "label": "Ciudadela La Inmaculada"},
    {"list_name": "list_sectores", "name": "las_brisas", "label": "Ciudadela Las Brisas"},
    {"list_name": "list_sectores", "name": "platanillos", "label": "Recinto Platanillos"},
    {"list_name": "list_sectores", "name": "panupali", "label": "Recinto Panupali"},
    {"list_name": "list_sectores", "name": "naranjos", "label": "Recinto Naranjos"},
    {"list_name": "list_sectores", "name": "san_jose", "label": "Recinto San José"},
    {"list_name": "list_sectores", "name": "fatima", "label": "Recinto Fátima"},
    {"list_name": "list_sectores", "name": "damas", "label": "Recinto Damas"},
    {"list_name": "list_sectores", "name": "otro", "label": "Otro recinto / comunidad"},

    # list_roles
    {"list_name": "list_roles", "name": "presidente_gad", "label": "Presidente del GAD Parroquial (Sr. Jorge Homero Ochoa Sánchez)"},
    {"list_name": "list_roles", "name": "vocal_gad", "label": "Vocal o funcionario del GAD Parroquial"},
    {"list_name": "list_roles", "name": "lider_comunitario", "label": "Líder comunitario / Representante de recinto"},
    {"list_name": "list_roles", "name": "salud_educacion", "label": "Personal de salud o directivo docente"},
    {"list_name": "list_roles", "name": "productor_agropecuario", "label": "Productor agropecuario (Caña, Maíz, Ganadería, Cacao)"},
    {"list_name": "list_roles", "name": "comerciante_gastronomico", "label": "Comerciante / Emprendedor gastronómico en La Y"},
    {"list_name": "list_roles", "name": "morador", "label": "Habitante / Morador de la parroquia"},
    {"list_name": "list_roles", "name": "otro", "label": "Otro"},

    # list_edad
    {"list_name": "list_edad", "name": "18_29", "label": "18 a 29 años"},
    {"list_name": "list_edad", "name": "30_45", "label": "30 a 45 años"},
    {"list_name": "list_edad", "name": "46_60", "label": "46 a 60 años"},
    {"list_name": "list_edad", "name": "mas_60", "label": "Más de 60 años"},

    # list_calidad_agua
    {"list_name": "list_calidad_agua", "name": "buena", "label": "Buena (tratada / apta para consumo)"},
    {"list_name": "list_calidad_agua", "name": "regular_entubada", "label": "Regular (agua entubada sin cloración constante)"},
    {"list_name": "list_calidad_agua", "name": "vertiente_quebrada", "label": "Vertiente / Quebrada sin tratamiento"},
    {"list_name": "list_calidad_agua", "name": "tanquero_compra", "label": "Compra de bidones / Tanquero"},

    # list_continuidad
    {"list_name": "list_continuidad", "name": "continua_24h", "label": "Continua las 24 horas del día"},
    {"list_name": "list_continuidad", "name": "parcial_horas", "label": "Parcial (ciertas horas al día)"},
    {"list_name": "list_continuidad", "name": "cortes_frecuentes", "label": "Intermitente con cortes frecuentes en invierno/verano"},

    # list_saneamiento
    {"list_name": "list_saneamiento", "name": "alcantarillado", "label": "Red pública de alcantarillado sanitario"},
    {"list_name": "list_saneamiento", "name": "pozo_septico", "label": "Pozo séptico individual"},
    {"list_name": "list_saneamiento", "name": "pozo_ciego_letrina", "label": "Pozo ciego / Letrina"},
    {"list_name": "list_saneamiento", "name": "descarga_rio", "label": "Descarga directa a estero, quebrada o río Saracay"},

    # list_recoleccion
    {"list_name": "list_recoleccion", "name": "diario", "label": "Diario"},
    {"list_name": "list_recoleccion", "name": "dos_tres_semana", "label": "2 a 3 veces por semana"},
    {"list_name": "list_recoleccion", "name": "semanal", "label": "1 vez por semana"},
    {"list_name": "list_recoleccion", "name": "irregular_quema", "label": "No pasa recolector (quema o entierro)"},

    # list_vias
    {"list_name": "list_vias", "name": "asfaltada_buena", "label": "Asfaltada en buen estado (Eje principal E585)"},
    {"list_name": "list_vias", "name": "lastrada_regular", "label": "Lastrada / Afirmada con baches"},
    {"list_name": "list_vias", "name": "critica_invierno", "label": "Mala / Intransitable en temporada lluviosa"},

    # list_internet
    {"list_name": "list_internet", "name": "fibra", "label": "Fibra óptica domiciliaria"},
    {"list_name": "list_internet", "name": "datos_moviles", "label": "Datos móviles celular"},
    {"list_name": "list_internet", "name": "sin_acceso", "label": "Sin acceso a internet"},

    # list_sino
    {"list_name": "list_sino", "name": "si", "label": "Sí"},
    {"list_name": "list_sino", "name": "no", "label": "No"},

    # list_actividades
    {"list_name": "list_actividades", "name": "cana_panela", "label": "Cultivo de caña de azúcar y molienda de panela"},
    {"list_name": "list_actividades", "name": "maiz_granos", "label": "Producción de maíz duro y granos"},
    {"list_name": "list_actividades", "name": "platano_cacao", "label": "Plátano y cacao fino de aroma"},
    {"list_name": "list_actividades", "name": "ganaderia_carne_leche", "label": "Ganadería bovina de carne y leche"},
    {"list_name": "list_actividades", "name": "comercio_gastronomia_la_y", "label": "Comercio gastronómico y paradores en La Y"},
    {"list_name": "list_actividades", "name": "transporte_servicios", "label": "Transporte interprovincial, mecánica y servicios"},

    # list_comercializacion
    {"list_name": "list_comercializacion", "name": "venta_la_y", "label": "Venta directa en paradores de La Y de Saracay"},
    {"list_name": "list_comercializacion", "name": "mercados_pinas_balsas", "label": "Mercados cantonales (Piñas, Balsas o Machala)"},
    {"list_name": "list_comercializacion", "name": "intermediario_finca", "label": "Intermediario a pie de finca"},
    {"list_name": "list_comercializacion", "name": "consumo_local", "label": "Consumo familiar y venta menor"},

    # list_nivel
    {"list_name": "list_nivel", "name": "alto", "label": "Alto"},
    {"list_name": "list_nivel", "name": "medio", "label": "Medio"},
    {"list_name": "list_nivel", "name": "bajo", "label": "Bajo"},

    # list_prioridades
    {"list_name": "list_prioridades", "name": "alcantarillado_ptar", "label": "Alcantarillado sanitario y Planta de Tratamiento de Aguas Residuales (PTAR)"},
    {"list_name": "list_prioridades", "name": "agua_potable_optimizacion", "label": "Optimización y ampliación de reservorios de agua potable"},
    {"list_name": "list_prioridades", "name": "vias_recintos", "label": "Asfaltado y mejoramiento vial a recintos (Platanillos, Panupali)"},
    {"list_name": "list_prioridades", "name": "ordenamiento_la_y", "label": "Ordenamiento urbano, drenaje y parador turístico en La Y"},
    {"list_name": "list_prioridades", "name": "salud_equipamiento", "label": "Ampliación y equipamiento del Centro de Salud"},
    {"list_name": "list_prioridades", "name": "defensas_rio", "label": "Muros de contención y defensas ribereñas en el río Saracay"}
]

# Crear y desplegar
payload_asset = {
    "name": "Diagnóstico Territorial y Saneamiento Básico - Parroquia Saracay (UNL)",
    "asset_type": "survey",
    "content": json.dumps({
        "schema": "1",
        "survey": survey,
        "choices": choices,
        "settings": {
            "title": "Diagnóstico Territorial Saracay - UNL",
            "id_string": "saracay_diagnostico_unl_2026"
        }
    })
}

print("1. Creando formulario en KoboToolbox...")
r_create = requests.post(f"{BASE_URL}/api/v2/assets/", headers=headers, json=payload_asset)
print("Create Status:", r_create.status_code)
uid = r_create.json().get("uid")
print("UID:", uid)

print("2. Desplegando formulario...")
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
    print("¡FORMULARIO OFICIAL DESPLEGADO EXITOSAMENTE!")
    print(f"UID del Formulario: {uid}")
    print(f"Enlace Web Enketo: {links.get('url')}")
    print(f"Enlace Único: {links.get('single_url')}")
    print(f"Enlace Offline: {links.get('offline_url')}")
    print("="*70)
else:
    print("Deploy text:", r_dep.text[:400])
