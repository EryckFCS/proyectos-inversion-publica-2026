* ==============================================================================
* PROYECTO: LEVANTAMIENTO DE INFORMACIÓN TERRITORIAL - PARROQUIA TORATA (EL ORO)
* ASIGNATURA: PROYECTOS DE INVERSIÓN PÚBLICA - SÉPTIMO CICLO
* INSTITUCIÓN: UNIVERSIDAD NACIONAL DE LOJA (CARRERA DE ECONOMÍA)
* AUTORES: Erick Condoy, David Pérez, Luis Hurtado, Lizeth Correa
* DOCENTE: Econ. José Job Chamba Tandazo
* FECHA: Octubre de 2026
* DO-FILE: 01_procesamiento_indicadores_torata.do
* ==============================================================================

clear all
set more off
capture log close

* ------------------------------------------------------------------------------
* 1. CONFIGURACIÓN DE DIRECTORIOS Y ENTORNO
* ------------------------------------------------------------------------------
* Detección dinámica del directorio del do-file para evitar ejecutar en C:\Program Files (x86)\Stata18
quietly {
    capture noisily {
        * Si se ejecuta desde el Do-file Editor de Stata:
        local script_path `"`c(filename)'"'
        if `"`script_path'"' != "" {
            local script_dir : file path `"`script_path'"'
            cd `"`script_dir'"'
        }
        else {
            * Ruta por defecto del repositorio si se invoca externamente
            cd "d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro/levantamiento_de_informacion/stata"
        }
    }
    if _rc != 0 {
        cd "d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro/levantamiento_de_informacion/stata"
    }
}

* Asegurar la existencia de las subcarpetas necesarias
capture mkdir "output"
capture mkdir "output/graphs"
capture mkdir "output/tables"
capture mkdir "data"

log using "output/01_procesamiento_indicadores.log", replace text

di as text "=================================================================="
di as text "PROCESAMIENTO DE LÍNEA BASE Y PROYECCIONES - TORATA (CENSO 2022)"
di as text "=================================================================="

* ------------------------------------------------------------------------------
* 2. DECLARACIÓN FORMAL DE FUENTES OFICIALES (BASE CENSAL INEC 2022 Y PDOT TORATA)
* ------------------------------------------------------------------------------
/*
DECLARACIÓN DE FUENTE PRIMARIA:
- Instituto Nacional de Estadística y Censos (INEC): VIII Censo de Población y VII de Vivienda 2022.
- Base de datos territorial REDATAM / DPA 070654 (Provincia de El Oro, Cantón Santa Rosa, Parroquia Torata).
- Población Base Oficial al Censo 2022: P_0 = 2.174 habitantes empadronados (1.109 hombres, 1.065 mujeres).
- Tasa oficial de crecimiento poblacional de la Parroquia Torata: r = +0.94% anual (+0.0094).
- Modelo demográfico adoptado: Crecimiento Geométrico Exponencial Discreto conforme a la metodología
  oficial de Planifica Ecuador y la Secretaría Nacional de Planificación:
  P_t = P_2022 * (1 + r)^(t), donde t = anio - 2022.
- Línea base de hogares: Densidad promedio de 3.6 miembros por hogar (PDOT Torata / Censo INEC 2022).
- Demanda referencial de viajes rurales de intercambio cantonal: 0.20 viajes/habitante/día.
*/

* ------------------------------------------------------------------------------
* 3. MÓDULO I: CREACIÓN Y CURACIÓN DE LA BASE DE INDICADORES TERRITORIALES (40 VARIABLES)
* ------------------------------------------------------------------------------

input str20 componente str35 variable str18 unidad double valor str25 fuente
"SOCIAL"        "Poblacion_Hombres"          "hab"          1109   "INEC_Censo_2022"
"SOCIAL"        "Poblacion_Mujeres"          "hab"          1065   "INEC_Censo_2022"
"SOCIAL"        "Poblacion_Total"            "hab"          2174   "INEC_Censo_2022"
"SOCIAL"        "Densidad_Poblacional"       "hab/km2"      25.46  "INEC_PDOT"
"SOCIAL"        "Estructura_0_14"            "%"            21.80  "INEC_PDOT_Tabla29"
"SOCIAL"        "Estructura_15_64"           "%"            67.71  "INEC_PDOT_Tabla29"
"SOCIAL"        "Estructura_65_mas"          "%"            10.49  "INEC_PDOT_Tabla29"
"SOCIAL"        "Autoidentificacion_Mestiza" "%"            92.40  "INEC_Censo_2022"
"SOCIAL"        "Autoidentificacion_Otras"   "%"            7.60   "INEC_Censo_2022"
"SOCIAL"        "Tasa_Crecimiento_Poblac"    "%"            0.94   "INEC_2022"
"SOCIAL"        "Escolaridad_Media"          "anios"        7.80   "INEC_Censo_2022"
"SOCIAL"        "Tasa_Alfabetizacion"        "%"            92.60  "INEC_Censo_2022"
"SOCIAL"        "Pobreza_NBI"                "%"            67.40  "INEC_Censo_2022"
"SOCIAL"        "Agua_Red_Entubada"          "%"            64.20  "EMAPASR_PDOT"
"SOCIAL"        "Alcantarillado"             "%"            28.50  "EMAPASR_PDOT"
"SOCIAL"        "Deficit_Sanitario"          "%"            71.50  "EMAPASR_PDOT"
"SOCIAL"        "Electricidad"               "%"            95.80  "CNEL_El_Oro"
"SOCIAL"        "Recoleccion_Desechos"       "%"            54.30  "GAD_Santa_Rosa"
"SOCIAL"        "Internet_Fijo"              "%"            38.70  "INEC_Censo_2022"
"SOCIAL"        "Establecimientos_Educativos" "unidades"    4      "Min_Educacion"
"SOCIAL"        "Establecimientos_Salud"     "unidades"     1      "MSP_07D06"
"SOCIAL"        "Tiempo_Acceso_Cantonal"     "minutos"      40     "Levantamiento_Campo"
"SOCIAL"        "Longitud_Red_Vial"          "km"           46.20  "MTOP_GAD"
"SOCIAL"        "Vias_Pavimentadas_Asfalto"  "%"            34.20  "PDOT_Torata"
"ECONOMICO"     "PEA_Total"                  "personas"     1241   "ENEMDU_PDOT_Torata"
"ECONOMICO"     "Empleo_Adecuado_Pleno"      "%"            18.10  "PDOT_Torata_Tabla64"
"ECONOMICO"     "Subempleo_No_Remunerado"    "%"            57.70  "PDOT_Torata_Tabla64"
"ECONOMICO"     "Desempleo_Abierto"          "%"            1.90   "PDOT_Torata_p172"
"ECONOMICO"     "Sector_Primario"            "%"            55.00  "PDOT_Torata_Tabla66"
"ECONOMICO"     "Sector_Secundario"          "%"            7.50   "PDOT_Torata_Tabla66"
"ECONOMICO"     "Sector_Terciario"           "%"            37.50  "PDOT_Torata_Tabla66"
"ECONOMICO"     "Unidades_Economicas_SRI"    "unidades"     42     "SRI_Santa_Rosa"
"ECONOMICO"     "Ingreso_Mensual_Hogar"      "USD/mes"      415.00 "Encuesta_GAD"
"ECONOMICO"     "Ganado_Bovino"              "cabezas"      3898   "PDOT_Torata_Tabla68"
"ECONOMICO"     "Produccion_Agricola"        "ton/anio"     1650   "MAG_El_Oro"
"ECONOMICO"     "Llegada_Excursionistas"     "vis/anio"     1200   "Turismo_GAD"
"ECONOMICO"     "Superficie_Agropecuaria"    "ha"           5240   "MAG_PDOT"
"AMBIENTAL"     "Superficie_ha"              "ha"           8538.0 "SIGTIERRAS_IGM"
"AMBIENTAL"     "Superficie_km2"             "km2"          85.38  "SIGTIERRAS_IGM"
"AMBIENTAL"     "Altitud_Media"              "msnm"         480    "SRTM_PDOT"
"AMBIENTAL"     "Pendiente_Relieve"          "%"            28.00  "PDOT_Torata"
"AMBIENTAL"     "Temperatura_Media"          "Celsius"      23.60  "INAMHI"
"AMBIENTAL"     "Precipitacion_Media"        "mm/anio"      1280.0 "INAMHI"
"AMBIENTAL"     "Bosque_Vegetacion_Nat"      "%"            27.20  "MAATE"
"AMBIENTAL"     "Pastizales_Pecuarios"       "%"            58.40  "MAG_MAATE"
"AMBIENTAL"     "Zonas_Recarga_Hidrica"      "ha"           1450.0 "EMAPASR_MAATE"
"AMBIENTAL"     "Area_Amenaza_Natural"       "%"            21.55  "SNGRE"
"AMBIENTAL"     "Amenazas_Prioritarias"      "unidades"     2      "Plan_Contingencia"
"AMBIENTAL"     "Caudal_Tomas_Agua"          "L/s"          32.50  "EMAPASR_EP"
"INSTITUCIONAL" "Organizaciones_Sociales"    "unidades"     11     "MIES_GADPR"
"INSTITUCIONAL" "Presupuesto_Anual_GAD"      "USD/anio"     260000 "Cedula_GADPR"
"INSTITUCIONAL" "Proyectos_Ejecutados"       "unidades"     6      "Rendicion_Cuentas"
"INSTITUCIONAL" "Instrumentos_Planificacion" "unidades"     2      "Registro_Oficial"
"INSTITUCIONAL" "Instituciones_Presencia"    "unidades"     6      "Directorio_GAD"
"INSTITUCIONAL" "Emprendimientos_Cooperat"   "unidades"     5      "MIPRO_GAD"
end

label var componente "Componente Multidimensional (Planifica Ecuador)"
label var variable "Variable de Línea Base Territorial"
label var unidad "Unidad de Medida Oficial"
label var valor "Valor Cuantitativo Oficial"
label var fuente "Fuente Oficial de Verificación"

save "data/base_curada_indicadores_torata.dta", replace
export delimited using "data/base_curada_indicadores_torata.csv", replace delimiter(",")
di as result "Base curada de indicadores guardada exitosamente."

* ------------------------------------------------------------------------------
* 4. MÓDULO II: PROYECCIONES DEMOGRÁFICAS BASADAS ESTRICTAMENTE EN CENSO 2022
* ------------------------------------------------------------------------------

scalar P_base_2022 = 2174
scalar r_oficial = 0.0094
scalar miembros_hogar = 3.6
scalar factor_viajes = 0.20

clear
set obs 21
gen int anio = 2022 + _n - 1
gen int t = anio - 2022
gen double pob_proyectada = P_base_2022 * ((1 + r_oficial)^t)
gen double hogares = pob_proyectada / miembros_hogar
gen double viajes_diarios = pob_proyectada * factor_viajes

format pob_proyectada %8.0f
format hogares %8.0f
format viajes_diarios %8.0f

label var anio "Año Calendario"
label var t "Horizonte de Planificación (t = anio - 2022)"
label var pob_proyectada "Población Proyectada (Base Censo 2022, r=0.94%)"
label var hogares "Hogares Estimados (3.6 personas/hogar)"
label var viajes_diarios "Demanda de Movilidad Rural (Viajes/día)"

save "data/proyecciones_demograficas_torata_2022_2042.dta", replace
export delimited using "data/proyecciones_demograficas_torata_2022_2042.csv", replace delimiter(",")

* Tabla quinquenal para inclusión en el reporte académico
preserve
keep if inlist(anio, 2022, 2024, 2026, 2028, 2030, 2032, 2034, 2036, 2038, 2040, 2042)
export delimited using "output/tables/tabla_proyecciones_quinquenales.csv", replace delimiter(",")
restore

di as result "Proyecciones 2022-2042 exportadas en .dta y .csv."

* ------------------------------------------------------------------------------
* 5. MÓDULO III: GENERACIÓN DE GRÁFICOS OFICIALES
* ------------------------------------------------------------------------------

* Gráfico 1: Proyección Demográfica
twoway (connected pob_proyectada anio, lcolor(navy) lwidth(medthick) mcolor(navy) msymbol(circle) msize(small)), ///
    title("Proyección Demográfica Parroquia Torata (2022-2042)", size(medium) color(black)) ///
    subtitle("Base Censo INEC 2022 (P0 = 2.174 hab; r = +0.94% anual)", size(small) color(gs6)) ///
    ytitle("Habitantes Empadronados", size(small)) ///
    xtitle("Año Calendario", size(small)) ///
    xlabel(2022(2)2042, labsize(small) grid) ///
    ylabel(2100(100)2700, labsize(small) grid) ///
    note("Fuente: Modelo Geométrico Stata con base en Censo INEC 2022.", size(vsmall)) ///
    graphregion(color(white)) bgcolor(white)

graph export "output/graphs/grafico_proyeccion_demografica_stata.png", width(1800) height(1200) replace

log close
