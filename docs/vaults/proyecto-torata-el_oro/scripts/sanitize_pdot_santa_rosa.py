import fitz
import os

pdf_path = "d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro/readings/02_instrumentos_planificacion_territorial/pdot_santa_rosa/Plan-de-Desarrollo-y-Ordenamiento-Territorial-del-canton-Santa-Rosa-2023-2027-2_actualizado.pdf"
out_dir = "d:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro/readings/02_instrumentos_planificacion_territorial/pdot_santa_rosa/sanitized"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print("Iniciando sanitización del PDOT Santa Rosa Actualizado (1014 páginas)...")

torata_pages = []
for p in range(len(doc)):
    txt = doc[p].get_text("text")
    if any(k in txt.lower() for k in ["torata", "playón", "playon", "guayabo", "la chilca"]):
        lines = [l.strip() for l in txt.split("\n") if l.strip()]
        torata_pages.append(f"<!-- PAGE {p+1} -->\n" + "\n".join(lines))

torata_content = "\n\n".join(torata_pages)
out_file = os.path.join(out_dir, "pdot_santa_rosa_2023_2027_extractos_torata_actualizado.md")

with open(out_file, "w", encoding="utf-8") as f:
    f.write("---\n")
    f.write("title: 'Plan de Desarrollo y Ordenamiento Territorial de Santa Rosa 2023-2027 (Actualizado 2024)'\n")
    f.write("canton: 'Santa Rosa'\n")
    f.write("provincia: 'El Oro'\n")
    f.write("fecha_actualizacion: 'Julio 2024'\n")
    f.write(f"paginas_relevantes: {len(torata_pages)}\n")
    f.write("---\n\n")
    f.write("# Extractos Sanitizados del PDOT Santa Rosa Actualizado (Secciones Vinculadas a Torata, El Playón y Conectividad Vial)\n\n")
    f.write(torata_content)

print(f"Sanitizado Torata generado: {len(torata_content)} caracteres en {len(torata_pages)} páginas.")

