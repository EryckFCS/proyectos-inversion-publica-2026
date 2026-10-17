import docx

doc = docx.Document()
h1 = doc.add_heading('UNIVERSIDAD NACIONAL DE LOJA', 1)
h1.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
h2 = doc.add_heading('FACULTAD JURÍDICA, SOCIAL Y ADMINISTRATIVA | CARRERA DE ECONOMÍA', 2)
h2.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
p_sub = doc.add_paragraph('Proyectos de Inversión Pública - Séptimo Ciclo | Docente: Econ. José Job Chamba Tandazo, Mg. Sc.')
p_sub.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
h3 = doc.add_heading('GUÍA DE ENTREVISTA A INFORMANTES CLAVE Y AUTORIDADES LOCALES\nDIAGNÓSTICO TERRITORIAL Y LÍNEA BASE PARA PROYECTOS DE INVERSIÓN', 3)
h3.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

p_prot = doc.add_paragraph('Buenos días/tardes. Somos estudiantes e investigadores de la Carrera de Economía de la Universidad Nacional de Loja. Estamos realizando un diagnóstico integral del territorio para construir la línea base socioeconómica, ambiental e institucional que fundamentará futuros proyectos de inversión pública en la Parroquia Saracay, Cantón Piñas, Provincia de El Oro. Agradecemos su valioso tiempo para responder a las siguientes preguntas según su conocimiento e información técnica sobre la localidad.')

# Sec 0 Table
t0 = doc.add_table(rows=3, cols=3)
t0.style = 'Table Grid'
t0.cell(0, 0).text = 'Provincia / Cantón / Parroquia:'
t0.cell(0, 1).text = 'El Oro / Piñas / Saracay'
t0.cell(0, 2).text = 'Fecha: 15 / 10 / 2026'
t0.cell(1, 0).text = 'Lugar / Sector:'
t0.cell(1, 1).text = 'Cabecera Parroquial Saracay (Sede del GAD Parroquial)'
t0.cell(1, 2).text = 'Hora inicio: 10:00'
t0.cell(2, 0).text = 'Entrevistado / Cargo:'
t0.cell(2, 1).text = 'Sr. Jorge Homero Ochoa Sánchez\nPresidente del GAD Parroquial Rural de Saracay (2023-2027)'
t0.cell(2, 2).text = 'Entrevistadora / Investigadora UNL:\nLizeth Camila Correa Sánchez'

# Mod I
doc.add_heading('MÓDULO I: CARACTERIZACIÓN GENERAL Y DATOS DEL TERRITORIO', 2)
doc.add_paragraph('1.1 Delimitación y Marco de Planificación Territorial:')
doc.add_paragraph('1.1.1 Denominación político-administrativa exacta:\nRespuesta: Parroquia Rural Saracay (creación municipal: 31 de marzo de 1989; demarcación CELIR: 28 de noviembre de 1995), perteneciente al Cantón Piñas, Provincia de El Oro (Código DPA INEC: 071056).')
doc.add_paragraph('1.1.2 Instrumentos de planificación vigentes:\n[X] Sí   [ ] No   [ ] En actualización\nEspecifique: Plan de Desarrollo y Ordenamiento Territorial (PDOT) de la Parroquia Saracay 2023-2027; articulado al PDOT del Cantón Piñas 2024-2027.')

doc.add_paragraph('1.2 Ubicación y Variables Biogeográficas de Entorno:')
t1 = doc.add_table(rows=6, cols=3)
t1.style = 'Table Grid'
t1.cell(0, 0).text = 'Variable Geográfica / Física'
t1.cell(0, 1).text = 'Dato Estimado / Registro Oficial'
t1.cell(0, 2).text = 'Unidad de Medida'
t1.cell(1, 0).text = 'Ubicación Geográfica'
t1.cell(1, 1).text = 'Noroccidente de Piñas (a 27 km de la cabecera cantonal), en el nodo vial "La Y" de Saracay'
t1.cell(1, 2).text = 'Referencia espacial'
t1.cell(2, 0).text = 'Superficie Oficial'
t1.cell(2, 1).text = '110,00 km² (11.000 ha)'
t1.cell(2, 2).text = 'km²'
t1.cell(3, 0).text = 'Rango Altitudinal'
t1.cell(3, 1).text = '220 a 450 m s.n.m. (estribaciones occidentales andinas y valle fluvial)'
t1.cell(3, 2).text = 'm s.n.m.'
t1.cell(4, 0).text = 'Temperatura Media'
t1.cell(4, 1).text = '22 a 26 °C (clima tropical cálido húmedo / subcálido)'
t1.cell(4, 2).text = '°C'
t1.cell(5, 0).text = 'Cuenca Hidrográfica'
t1.cell(5, 1).text = 'Cuenca del Río Saracay, Río Fátima, Río Naranjos y afluentes'
t1.cell(5, 2).text = 'Red hídrica'

doc.add_paragraph('1.3 Asentamientos Humanos y Conectividad Vial:')
doc.add_paragraph('1.3.1 Distribución espacial de asentamientos: Cabecera urbana (ciudadelas El Bosque, El Tamarindo, La Inmaculada, La Central, Las Brisas, La Y, La Florida) y 11 recintos rurales (Platanillos, Panupali, Naranjos, San José, Fátima, El Triunfo, Las Orquídeas, Las Palmas, Camarones, La Unión, Damas).')
doc.add_paragraph('1.3.2 Vías de articulación: Nodo vial estratégico interprovincial "La Y" de Saracay (conexión de la Troncal E25 / E585 entre Costa, Altiplano Ourense Piñas-Zaruma y la Provincia de Loja vía Balsas). Vías secundarias lastradas hacia recintos.')

# Mod II
doc.add_heading('MÓDULO II: COMPONENTE SOCIO-CULTURAL Y ACCESO A SERVICIOS BÁSICOS', 2)
doc.add_paragraph('2.1 Demografía y Hogares:')
doc.add_paragraph('2.1.1 Población Censo 2022: 2.775 habitantes censados (Censo 2010: 2.545 habitantes; tasa intercensal geométrica: +0,724% anual). Densidad bruta: 25,23 hab/km².')
doc.add_paragraph('2.2 Servicios Básicos:')
doc.add_paragraph('2.2.1 Agua para consumo humano: Sistema por red matriz y reservorios en el casco urbano central coordinado con EPAA-Piñas; fuentes de vertientes y quebradas en recintos. Problemas de turbiedad en invierno y continuidad del suministro.')
doc.add_paragraph('2.2.2 Saneamiento y alcantarillado: Red de alcantarillado combinada y parcial en la cabecera parroquial; carencia de Planta de Tratamiento de Aguas Residuales (PTAR); predominio de pozos sépticos y letrinas en recintos rurales.')
doc.add_paragraph('2.2.3 Desechos sólidos: Servicio de recolección articulado con el GAD Municipal de Piñas.')
doc.add_paragraph('2.2.4 Salud y educación: 1 Centro de Salud Rural del MSP en la cabecera parroquial; Unidad Educativa Saracay y planteles de educación básica en los recintos.')

# Mod III
doc.add_heading('MÓDULO III: COMPONENTE ECONÓMICO-PRODUCTIVO Y AMBIENTAL', 2)
doc.add_paragraph('3.1 Estructura Productiva:')
doc.add_paragraph('3.1.1 Actividad agropecuaria: Concentra el 58% de la población ocupada. Principales rubros: Caña de azúcar (molienda de panela), maíz duro, plátano, cacao fino de aroma, cítricos (naranja, mandarina, limón) y café.')
doc.add_paragraph('3.1.2 Comercio, transporte y servicios: 32% de la PEA ocupada, dinamizada por el nodo vial "La Y" de Saracay (paraderos gastronómicos, transporte interprovincial y talleres).')
doc.add_paragraph('3.1.3 Ganadería y pecuaria: 7% ganadería bovina (carne y doble propósito) y porcicultura.')
doc.add_paragraph('3.1.4 Manufactura artesanal: 3% en moliendas paneleras y manufactura menor.')
doc.add_paragraph('3.2 Atractivos Naturales y Recursos Hídricos:')
doc.add_paragraph('3.2.1 Balnearios fluviales y microcuencas: Riberas del río Saracay, río Fátima y cascadas locales, con potencial recreativo y ecoturístico pero vulnerables a vertidos de aguas servidas sin tratamiento.')

# Mod IV
doc.add_heading('MÓDULO IV: DEMANDA DE INVERSIÓN PÚBLICA Y VALIDACIÓN TERRITORIAL', 2)
doc.add_paragraph('4.1 Principales Cuellos de Botella Identificados para Indagación:')
doc.add_paragraph('1. Construcción y mejoramiento del sistema de alcantarillado sanitario y Planta de Tratamiento de Aguas Residuales (PTAR) para evitar descargas crudas al río Saracay.')
doc.add_paragraph('2. Optimización y ampliación del sistema de agua potable, capacidad de reservorios y desinfección continua.')
doc.add_paragraph('3. Mantenimiento y asfaltado de ramales viales que conectan los recintos productivos (Platanillos, Panupali, Naranjos) con la vía principal.')
doc.add_paragraph('4. Fortalecimiento del parador turístico-gastronómico y ordenamiento urbano en el sector "La Y".')
doc.add_paragraph('4.2 Cartera de Proyectos Activos y Ejecutados en el Territorio (2023-2026):')
doc.add_paragraph('1. Construcción de nuevo Tanque Reservorio de Agua Potable para el Casco Central de Saracay: En ejecución por el GAD Municipal de Piñas en convenio con la Junta Administradora de Agua (Presidida por el Sr. Manuel Salazar).')
doc.add_paragraph('2. Programa de Dotación de Filtros Purificadores Domiciliarios de Agua: Ejecutado por el GAD Municipal de Piñas con cooperación internacional para familias en zonas vulnerables.')
doc.add_paragraph('3. Rehabilitación Integral y Bacheo Tecnificado de los 28 km del Eje Vial Estatal Piñas-Saracay (E585): En ejecución activa mediante convenio tripartito entre MTOP/MIT, Prefectura de El Oro y GADM Piñas (puntos críticos: Las Bateas, Monos, Naranjos y Panupali).')
doc.add_paragraph('4. Mantenimiento y Apertura de Caminos Vecinales Rurales: En ejecución continua por el GAD Parroquial Rural de Saracay en coordinación con la Prefectura hacia recintos como Platanillos, Panupali, Damas y Fátima.')
doc.add_paragraph('5. Construcción de Paradas de Buses y Adecuación de Espacios Comunitarios en La Y y Casco Central: Ejecutado por el GAD Parroquial de Saracay.')
doc.add_paragraph('6. Proyecto Propuesto UNL: Estudio Técnico y Formulación del Sistema de Alcantarillado Sanitario y PTAR para resolver la contaminación de la cuenca del río Saracay (déficit del 68,5%).')

out_doc = r'd:\07_Ciclo\septimo_ciclo\public_investment_projects\docs\vaults\proyecto-saracay\levantamiento_de_informacion\Guia_Entrevista_Diagnostico_Saracay_ElOro.docx'
doc.save(out_doc)
print('Guía Word diligenciada con éxito en:', out_doc)
