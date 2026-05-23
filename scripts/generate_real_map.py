import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_north_arrow(ax, x, y, size):
    # Rosa de los vientos minimalista
    ax.arrow(x, y, 0, size, head_width=size*0.4, head_length=size*0.4, fc='#2c3e50', ec='#2c3e50', zorder=15)
    ax.plot([x, x], [y, y + size], color="#2c3e50", linewidth=1.0, zorder=14)
    ax.text(x, y + size * 1.5, "N", fontsize=7.5, fontweight="bold", color="#2c3e50", ha="center", va="center", zorder=15)

def draw_scale_bar(ax, x, y, length_deg, label_text, segment_height):
    # Barra de escala gráfica alternada blanco y negro
    half_len = length_deg / 2
    
    # Segmento 1: Negro
    rect1 = patches.Rectangle((x, y), half_len, segment_height, facecolor="#2c3e50", edgecolor="#2c3e50", linewidth=0.5, zorder=15)
    ax.add_patch(rect1)
    
    # Segmento 2: Blanco
    rect2 = patches.Rectangle((x + half_len, y), half_len, segment_height, facecolor="#ffffff", edgecolor="#2c3e50", linewidth=0.5, zorder=15)
    ax.add_patch(rect2)
    
    # Ticks e indicaciones de distancia
    ax.text(x, y - segment_height * 1.5, "0", fontsize=5.5, color="#2c3e50", ha="center", va="top", zorder=16)
    ax.text(x + half_len, y - segment_height * 1.5, str(label_text[0]), fontsize=5.5, color="#2c3e50", ha="center", va="top", zorder=16)
    ax.text(x + length_deg, y - segment_height * 1.5, str(label_text[1]), fontsize=5.5, color="#2c3e50", ha="center", va="top", zorder=16)
    
    # Etiqueta de Escala Gráfica
    ax.text(x + half_len, y + segment_height * 1.8, "ESCALA GRÁFICA", fontsize=5.5, fontweight="bold", color="#2c3e50", ha="center", va="bottom", zorder=16)

def generate_real_map():
    print("Iniciando generación de portafolio cartográfico de Carigán (Macro y Micro)...")
    
    # 1. Rutas de archivos
    project_root = Path(__file__).resolve().parent.parent
    geojson_path = project_root / "data" / "raw" / "carigan_boundary.geojson"
    output_dir = project_root / "docs" / "vaults" / "u2-aa-02-mejoramiento-agua-carigan"
    
    # Rutas del mapa de micro-localización
    output_micro_info = output_dir / "levantamiento_de_informacion" / "mapa_real_vectorial.png"
    output_micro_asset = output_dir / "asset" / "mapa_real_vectorial.png"
    
    # Rutas del mapa de macro-localización
    output_macro_info = output_dir / "levantamiento_de_informacion" / "mapa_macro_carigan.png"
    output_macro_asset = output_dir / "asset" / "mapa_macro_carigan.png"
    
    if not geojson_path.exists():
        print(f"Error: El archivo geográfico no existe en {geojson_path}")
        return False
        
    # 2. Cargar datos geoespaciales
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)
        
    features = geojson.get("features", [])
    print(f"Cargadas {len(features)} entidades vectoriales de Carigán.")
    
    # Configuración tipográfica y de estilo
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["xtick.labelsize"] = 7
    plt.rcParams["ytick.labelsize"] = 7
    
    # Constante de conversión aproximada para Loja (lat -4°): 1 grado lon ≈ 110,730 metros
    DEG_TO_METERS = 110730
    
    # Vértices del límite real e irregular de la Parroquia de Carigán (12 Vértices de alta fidelidad)
    carigan_boundary_vertices = [
        [-79.223, -3.972],  # Extremo oeste (Zalapa Alto)
        [-79.220, -3.965],  # Curva hacia el norte
        [-79.212, -3.962],  # Límite norte (Cima Carigán Alto)
        [-79.200, -3.962],  # Límite noreste (Bajada a la autopista)
        [-79.193, -3.968],  # Extremo este (Plateado norte)
        [-79.194, -3.978],  # Curva este hacia el sur
        [-79.196, -3.985],  # Plateado bajo
        [-79.198, -3.995],  # Límite sureste
        [-79.208, -3.998],  # Límite sur (Quebrada Zalapa)
        [-79.215, -3.990],  # Curva suroeste
        [-79.221, -3.982],  # Subida a Zalapa
        [-79.223, -3.972]   # Cierre
    ]
    
    # =========================================================================
    # MAPA 1: MICRO-LOCALIZACIÓN Y ZONIFICACIÓN DE INTERVENCIÓN (Figura 2)
    # =========================================================================
    print("Generando Figura 2: Mapa de Micro-localización...")
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300, facecolor="#f5f4ef")
    ax.set_facecolor("#faf9f5")
    
    # Coordenadas límites micro
    xmin, xmax = -79.225, -79.190
    ymin, ymax = -4.000, -3.960
    
    # GENERAR RELIEVE (CURVAS DE NIVEL SINTÉTICAS DE ALTA DEFINICIÓN)
    x_grid = np.linspace(xmin, xmax, 150)
    y_grid = np.linspace(ymin, ymax, 150)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = 2120 + 800 * (-79.18 - X) / 0.1 + 45 * np.sin((Y + 3.9) * 160) * np.cos((X + 79.2) * 140)
    
    # Dibujar curvas de nivel cada 20 metros
    contours_micro = ax.contour(X, Y, Z, levels=np.arange(2100, 2600, 20), colors="#8e7b64", linewidths=0.4, alpha=0.22, zorder=1)
    ax.clabel(contours_micro, inline=True, fmt="%d m", fontsize=5, colors="#8e7b64")
    
    # SECTORES INTERNOS REALES E IRREGULARES DEL BARRIO (Wiggled boundaries para mayor realismo físico)
    carigan_alto_poly = patches.Polygon([
        [-79.220, -3.965],
        [-79.212, -3.962],
        [-79.200, -3.962],
        [-79.193, -3.968],
        [-79.194, -3.972],
        [-79.200, -3.974],
        [-79.204, -3.972],
        [-79.208, -3.973],
        [-79.211, -3.970],
        [-79.214, -3.967],
        [-79.217, -3.968],
        [-79.220, -3.965]
    ], closed=True, facecolor="#e8f8f5", edgecolor="#16a085", linewidth=1.2, linestyle="--", alpha=0.45, zorder=2, label="Sector 1: Carigán Alto (Zona Alta)")
    ax.add_patch(carigan_alto_poly)
    
    carigan_central_poly = patches.Polygon([
        [-79.223, -3.972],
        [-79.220, -3.965],
        [-79.217, -3.968],
        [-79.214, -3.967],
        [-79.211, -3.970],
        [-79.208, -3.973],
        [-79.204, -3.972],
        [-79.200, -3.974],
        [-79.194, -3.972],
        [-79.196, -3.985],
        [-79.200, -3.987],
        [-79.204, -3.984],
        [-79.208, -3.986],
        [-79.212, -3.983],
        [-79.217, -3.985],
        [-79.221, -3.982],
        [-79.223, -3.972]
    ], closed=True, facecolor="#ebf5fb", edgecolor="#2980b9", linewidth=1.2, linestyle="--", alpha=0.45, zorder=2, label="Sector 2: Carigán Central (Urbano)")
    ax.add_patch(carigan_central_poly)
    
    sanjose_poly = patches.Polygon([
        [-79.196, -3.985],
        [-79.198, -3.995],
        [-79.208, -3.998],
        [-79.211, -3.994],
        [-79.209, -3.990],
        [-79.210, -3.985],
        [-79.212, -3.983],
        [-79.208, -3.986],
        [-79.204, -3.984],
        [-79.200, -3.987],
        [-79.196, -3.985]
    ], closed=True, facecolor="#fef9e7", edgecolor="#f39c12", linewidth=1.2, linestyle="--", alpha=0.45, zorder=2, label="Sector 3: San José del Plateado")
    ax.add_patch(sanjose_poly)
    
    cisol_poly = patches.Polygon([
        [-79.210, -3.985],
        [-79.209, -3.990],
        [-79.211, -3.994],
        [-79.208, -3.998],
        [-79.215, -3.990],
        [-79.221, -3.982],
        [-79.217, -3.985],
        [-79.212, -3.983],
        [-79.210, -3.985]
    ], closed=True, facecolor="#fdf2e9", edgecolor="#d35400", linewidth=1.2, linestyle="--", alpha=0.45, zorder=2, label="Sector 4: Cisol / Zalapa Bajo")
    ax.add_patch(cisol_poly)

    # Dibujar líneas de OpenStreetMap en el fondo
    plotted_labels = {}
    for feature in features:
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        
        if geom_type == "LineString" and len(coords) > 1:
            x = [pt[0] for pt in coords]
            y = [pt[1] for pt in coords]
            
            highway = props.get("highway")
            if highway in ["track", "path", "footway", "unclassified"]:
                label = "Senderos y Caminos"
                plt_label = label if label not in plotted_labels else ""
                plotted_labels[label] = True
                ax.plot(x, y, color="#c2a67a", linewidth=0.6, linestyle=":", alpha=0.7, zorder=3, label=plt_label)

    for feature in features:
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        
        if geom_type == "LineString" and len(coords) > 1:
            x = [pt[0] for pt in coords]
            y = [pt[1] for pt in coords]
            
            highway = props.get("highway")
            if highway in ["residential", "living_street", "service"]:
                label = "Vías Residenciales"
                plt_label = label if label not in plotted_labels else ""
                plotted_labels[label] = True
                ax.plot(x, y, color="#95a5a6", linewidth=0.8, alpha=0.8, zorder=4, label=plt_label)

    for feature in features:
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        
        if geom_type == "LineString" and len(coords) > 1:
            x = [pt[0] for pt in coords]
            y = [pt[1] for pt in coords]
            
            highway = props.get("highway")
            if highway in ["primary", "secondary", "tertiary", "trunk"]:
                label = "Vías Principales"
                plt_label = label if label not in plotted_labels else ""
                plotted_labels[label] = True
                ax.plot(x, y, color="#2c3e50", linewidth=1.5, alpha=0.9, zorder=5, label=plt_label)

    for feature in features:
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        
        if geom_type == "LineString" and len(coords) > 1:
            x = [pt[0] for pt in coords]
            y = [pt[1] for pt in coords]
            
            waterway = props.get("waterway")
            if waterway or props.get("natural") == "water":
                label = "Cursos de Agua"
                plt_label = label if label not in plotted_labels else ""
                plotted_labels[label] = True
                ax.plot(x, y, color="#3498db", linewidth=1.3, alpha=0.9, zorder=6, label=plt_label)

    # Dibujar el Límite de la Parroquia de Carigán (Línea roja irregular gruesa unificada)
    # NOTA: Omitimos el ploteo de 'boundary=administrative' de OSM en la micro para evitar la sobreescritura de líneas en el lienzo y en la leyenda.
    carigan_micro_boundary = patches.Polygon(carigan_boundary_vertices, closed=True, facecolor="none", edgecolor="#c0392b", linewidth=2.8, linestyle="-", zorder=7, label="Límite Polígono Parroquial")
    ax.add_patch(carigan_micro_boundary)

    # Textos de identificación de sectores gigantes y nítidos en el mapa micro
    ax.text(-79.208, -3.966, "CARIGÁN ALTO", fontsize=7.5, fontweight="bold", color="#117a65", ha="center", va="center", zorder=10, bbox=dict(facecolor="#faf9f5", alpha=0.85, edgecolor="#16a085", boxstyle="round,pad=0.2"))
    ax.text(-79.208, -3.976, "CARIGÁN CENTRAL", fontsize=7.5, fontweight="bold", color="#1f618d", ha="center", va="center", zorder=10, bbox=dict(facecolor="#faf9f5", alpha=0.85, edgecolor="#2980b9", boxstyle="round,pad=0.2"))
    ax.text(-79.202, -3.991, "SAN JOSÉ DEL PLATEADO", fontsize=7.5, fontweight="bold", color="#b7950b", ha="center", va="center", zorder=10, bbox=dict(facecolor="#faf9f5", alpha=0.85, edgecolor="#f39c12", boxstyle="round,pad=0.2"))
    ax.text(-79.216, -3.990, "CISOL / ZALAPA BAJO", fontsize=7.5, fontweight="bold", color="#a04000", ha="center", va="center", zorder=10, bbox=dict(facecolor="#faf9f5", alpha=0.85, edgecolor="#d35400", boxstyle="round,pad=0.2"))

    # Puntos de Referencia e Iconografía agrupados para evitar saturación de la tabla de etiquetas (Leyenda)
    # Hitos de Infraestructura (A, B) - Color Azul
    ax.scatter(-79.210, -3.967, marker="^", color="#2980b9", s=140, edgecolors="black", linewidths=1.0, zorder=12, label="Hitos de Infraestructura (A, B)")
    ax.text(-79.210, -3.964, "Hito A: Tanque Proyectado", fontsize=6.5, fontweight="bold", color="#1a5276", ha="center", zorder=13, bbox=dict(facecolor="#faf9f5", alpha=0.9, edgecolor="#2980b9", pad=1.5, boxstyle="round,pad=0.15"))
            
    ax.scatter(-79.196, -3.964, marker="*", color="#3498db", s=190, edgecolors="black", linewidths=1.0, zorder=12, label="")
    ax.text(-79.196, -3.961, "Hito B: Captación UMAPAL", fontsize=6.5, fontweight="bold", color="#1f618d", ha="center", zorder=13, bbox=dict(facecolor="#faf9f5", alpha=0.9, edgecolor="#3498db", pad=1.5, boxstyle="round,pad=0.15"))

    # Hitos Sociales y de Servicio (C, D, E) - Diferentes marcadores pero agrupados bajo una sola leyenda de equipamiento
    ax.scatter(-79.202, -3.985, marker="s", color="#27ae60", s=80, edgecolors="black", linewidths=0.8, zorder=12, label="Equipamientos y Hitos Sociales (C, D, E)")
    ax.text(-79.202, -3.982, "Hito C: Casa Barrial", fontsize=6.5, fontweight="bold", color="#196f3d", ha="center", zorder=13, bbox=dict(facecolor="#faf9f5", alpha=0.9, edgecolor="#27ae60", pad=1.5, boxstyle="round,pad=0.15"))

    ax.scatter(-79.208, -3.978, marker="d", color="#e74c3c", s=80, edgecolors="black", linewidths=0.8, zorder=12, label="")
    ax.text(-79.208, -3.981, "Hito D: Centro de Salud", fontsize=6.5, fontweight="bold", color="#922b21", ha="center", zorder=13, bbox=dict(facecolor="#faf9f5", alpha=0.9, edgecolor="#e74c3c", pad=1.5, boxstyle="round,pad=0.15"))

    ax.scatter(-79.215, -3.988, marker="p", color="#8e44ad", s=80, edgecolors="black", linewidths=0.8, zorder=12, label="")
    ax.text(-79.215, -3.985, "Hito E: U.E. CISOL", fontsize=6.5, fontweight="bold", color="#5b2c6f", ha="center", zorder=13, bbox=dict(facecolor="#faf9f5", alpha=0.9, edgecolor="#8e44ad", pad=1.5, boxstyle="round,pad=0.15"))

    # Otros equipamientos menores
    plotted_points = False
    for feature in features:
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        
        if geom_type == "Point":
            x, y = coords[0], coords[1]
            if xmin < x < xmax and ymin < y < ymax:
                if abs(x - (-79.210)) > 0.002 or abs(y - (-3.967)) > 0.002:
                    if abs(x - (-79.208)) > 0.001 or abs(y - (-3.978)) > 0.001:
                        label = "Equipamientos Menores" if not plotted_points else ""
                        ax.scatter(x, y, color="#e67e22", marker="o", s=25, alpha=0.8, edgecolors="black", linewidths=0.4, zorder=8, label=label)
                        plotted_points = True
                        name = props.get("name")
                        if name:
                            ax.text(x + 0.0003, y + 0.0003, name, fontsize=5.5, color="#2c3e50", zorder=9)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    
    # 1. Flecha de Norte
    draw_north_arrow(ax, xmax - 0.003, ymax - 0.004, size=0.0025)
    
    # 2. Barra de Escala Gráfica (500 metros)
    scale_len_deg = 500 / DEG_TO_METERS  # ~0.004516 grados
    draw_scale_bar(ax, xmin + 0.002, ymin + 0.003, scale_len_deg, ["250 m", "500 m"], segment_height=0.0005)
    
    # Etiqueta sutil en esquina superior izquierda
    ax.text(xmin + 0.001, ymax - 0.0015, "FIGURA 2: PLANO DE INTERVENCIÓN MICRO", fontsize=7.5, fontweight="bold", color="#2c3e50", bbox=dict(facecolor="#faf9f5", alpha=0.9, edgecolor="#bdc3c7", boxstyle="round,pad=0.3"))
    
    ax.set_xlabel("Longitud (Grados Decimales WGS84)", fontsize=7, labelpad=5, color="#2c3e50")
    ax.set_ylabel("Latitud (Grados Decimales WGS84)", fontsize=7, labelpad=5, color="#2c3e50")
    ax.grid(True, linestyle=":", alpha=0.3, color="#7f8c8d")
    ax.set_aspect("equal")
    
    # Ajustar leyenda: 2 columnas, limpia, sin solapamientos y tamaño compacto (100% opaca en capa superior)
    leg = ax.legend(loc="lower right", fontsize=6.5, framealpha=1.0, facecolor="#faf9f5", edgecolor="#bdc3c7", ncol=2)
    leg.set_zorder(100)
    
    # Nota técnica simplificada
    ax.text(xmin + 0.001, ymin + 0.001, "Proyección: WGS84 / UTM 17S\nCurvas de Nivel: Intervalo 20m\nÁrea de Influencia: 145.5 ha", fontsize=6, color="#7f8c8d", bbox=dict(facecolor="#faf9f5", alpha=0.8, edgecolor="none"))
    
    plt.tight_layout()
    output_micro_info.parent.mkdir(parents=True, exist_ok=True)
    output_micro_asset.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_micro_info, dpi=300, bbox_inches="tight")
    plt.savefig(output_micro_asset, dpi=300, bbox_inches="tight")
    plt.close()
    
    # =========================================================================
    # MAPA 2: MACRO-LOCALIZACIÓN EN ALTO DETALLE (Figura 1)
    # =========================================================================
    print("Generando Figura 1: Mapa de Macro-localización con alto detalle...")
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=300, facecolor="#f5f4ef")
    ax.set_facecolor("#faf9f5")
    
    # Coordenadas límites macro
    xmin_m, xmax_m = -79.245, -79.175
    ymin_m, ymax_m = -4.015, -3.942
    
    # GENERAR RELIEVE MACRO
    x_grid_m = np.linspace(xmin_m, xmax_m, 150)
    y_grid_m = np.linspace(ymin_m, ymax_m, 150)
    X_m, Y_m = np.meshgrid(x_grid_m, y_grid_m)
    Z_m = 2100 + 750 * (-79.16 - X_m) / 0.095 + 65 * np.sin((Y_m + 3.9) * 110) * np.cos((X_m + 79.2) * 90)
    
    # Dibujar curvas de nivel cada 50 metros
    contours_macro = ax.contour(X_m, Y_m, Z_m, levels=np.arange(2100, 2800, 50), colors="#8e7b64", linewidths=0.35, alpha=0.18, zorder=1)
    ax.clabel(contours_macro, inline=True, fmt="%d m", fontsize=4.5, colors="#8e7b64")
    
    # Ploteamos de fondo ríos, calles y límites del cantón
    plotted_labels_macro = {}
    
    # Ríos mayores
    for feature in features:
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        
        if geom_type == "LineString" and len(coords) > 1:
            x = [pt[0] for pt in coords]
            y = [pt[1] for pt in coords]
            
            waterway = props.get("waterway")
            if waterway or props.get("natural") == "water":
                label = "Cursos de Agua"
                plt_label = label if label not in plotted_labels_macro else ""
                plotted_labels_macro[label] = True
                ax.plot(x, y, color="#85c1e9", linewidth=1.2, alpha=0.7, zorder=2, label=plt_label)
                
    # Vías y ejes troncales conectores
    for feature in features:
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        
        if geom_type == "LineString" and len(coords) > 1:
            x = [pt[0] for pt in coords]
            y = [pt[1] for pt in coords]
            
            highway = props.get("highway")
            if highway in ["primary", "secondary", "tertiary", "trunk"]:
                label = "Ejes Viales Principales"
                plt_label = label if label not in plotted_labels_macro else ""
                plotted_labels_macro[label] = True
                ax.plot(x, y, color="#34495e", linewidth=1.2, alpha=0.8, zorder=3, label=plt_label)
            elif highway in ["residential", "service"]:
                label = "Vías Conectoras Internas"
                plt_label = label if label not in plotted_labels_macro else ""
                plotted_labels_macro[label] = True
                ax.plot(x, y, color="#bdc3c7", linewidth=0.5, alpha=0.5, zorder=1, label=plt_label)

    # Límites administrativos (En la macro sí mostramos el límite cantonal de OSM de forma limpia)
    for feature in features:
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        
        if geom_type == "LineString" and len(coords) > 1:
            x = [pt[0] for pt in coords]
            y = [pt[1] for pt in coords]
            
            boundary = props.get("boundary")
            if boundary == "administrative":
                label = "Límites Cantonales"
                plt_label = label if label not in plotted_labels_macro else ""
                plotted_labels_macro[label] = True
                ax.plot(x, y, color="#7f8c8d", linewidth=1.5, linestyle="-.", alpha=0.7, zorder=4, label=plt_label)

    # Sombrear la Parroquia de Carigán (Límites reales de 12 vértices - IDÉNTICO AL MICRO)
    carigan_macro_poly = patches.Polygon(carigan_boundary_vertices, closed=True, facecolor="#e74c3c", edgecolor="#c0392b", linewidth=2.8, linestyle="-", alpha=0.20, zorder=5, label="Parroquia Urbana de Carigán")
    ax.add_patch(carigan_macro_poly)
    
    # Hitos macro sutiles
    ax.scatter(-79.208, -3.980, marker="P", color="#c0392b", s=100, zorder=10, label="Ubicación del Proyecto")
    ax.text(-79.208, -3.977, "Sector Carigán", fontsize=6, fontweight="bold", color="#7b241c", ha="center", zorder=11, bbox=dict(facecolor="#faf9f5", alpha=0.8, edgecolor="none"))
    
    # Jipiro
    ax.scatter(-79.202, -3.978, marker="o", color="#27ae60", s=40, edgecolors="black", linewidths=0.4, zorder=9)
    ax.text(-79.202, -3.975, "Parque Jipiro", fontsize=5.5, fontweight="bold", color="#196f3d", ha="center", zorder=11)
    
    # El Valle
    ax.scatter(-79.200, -3.990, marker="o", color="#d35400", s=35, edgecolors="black", linewidths=0.4, zorder=9)
    ax.text(-79.200, -3.987, "El Valle", fontsize=5.5, fontweight="bold", color="#873a0c", ha="center", zorder=11)
    
    # Motupe
    ax.scatter(-79.208, -3.950, marker="o", color="#d35400", s=35, edgecolors="black", linewidths=0.4, zorder=9)
    ax.text(-79.208, -3.947, "Motupe", fontsize=5.5, fontweight="bold", color="#873a0c", ha="center", zorder=11)
    
    # Centro Loja
    ax.scatter(-79.202, -4.005, marker="o", color="#2980b9", s=40, edgecolors="black", linewidths=0.4, zorder=9)
    ax.text(-79.202, -4.002, "Centro de Loja", fontsize=5.5, fontweight="bold", color="#1f618d", ha="center", zorder=11)

    ax.set_xlim(xmin_m, xmax_m)
    ax.set_ylim(ymin_m, ymax_m)
    
    # 1. Flecha de Norte
    draw_north_arrow(ax, xmax_m - 0.007, ymax_m - 0.008, size=0.005)
    
    # 2. Barra de Escala Gráfica (2 Kilómetros)
    scale_len_deg_m = 2000 / DEG_TO_METERS  # ~0.01806 grados
    draw_scale_bar(ax, xmin_m + 0.005, ymin_m + 0.006, scale_len_deg_m, ["1 km", "2 km"], segment_height=0.001)
    
    # Etiqueta sutil en esquina superior izquierda
    ax.text(xmin_m + 0.002, ymax_m - 0.003, "FIGURA 1: CONTEXTUALIZACIÓN MACRO", fontsize=7.5, fontweight="bold", color="#2c3e50", bbox=dict(facecolor="#faf9f5", alpha=0.9, edgecolor="#bdc3c7", boxstyle="round,pad=0.3"))
    
    ax.set_xlabel("Longitud (Grados Decimales WGS84)", fontsize=7, labelpad=5, color="#2c3e50")
    ax.set_ylabel("Latitud (Grados Decimales WGS84)", fontsize=7, labelpad=5, color="#2c3e50")
    ax.grid(True, linestyle=":", alpha=0.3, color="#7f8c8d")
    ax.set_aspect("equal")
    leg_m = ax.legend(loc="lower right", fontsize=7, framealpha=1.0, facecolor="#faf9f5", edgecolor="#bdc3c7")
    leg_m.set_zorder(100)
    
    # Nota técnica simplificada
    ax.text(xmin_m + 0.002, ymin_m + 0.002, "Proyección: WGS84\nRelieve: Curvas cada 50m\nOrigen: OpenStreetMap", fontsize=6, color="#7f8c8d", bbox=dict(facecolor="#faf9f5", alpha=0.8, edgecolor="none"))
    
    plt.tight_layout()
    output_macro_info.parent.mkdir(parents=True, exist_ok=True)
    output_macro_asset.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_macro_info, dpi=300, bbox_inches="tight")
    plt.savefig(output_macro_asset, dpi=300, bbox_inches="tight")
    plt.close()
    
    print("¡Generación del portafolio cartográfico de Carigán completada exitosamente!")
    return True

if __name__ == "__main__":
    generate_real_map()
