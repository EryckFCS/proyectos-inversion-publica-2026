import sys
from pathlib import Path

# Add project src and library src to path for absolute resolution
VAULT_DIR = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/u2-aa-02-mejoramiento-agua-carigan")
PROJECT_ROOT = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/public_investment_projects")
LIB_ROOT = Path("/home/erick-fcs/Capital_Workstation/capital-workstation-libs/src")

if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.append(str(PROJECT_ROOT / "src"))
if str(LIB_ROOT) not in sys.path:
    sys.path.append(str(LIB_ROOT))

from ecs_quantitative.management.intelligence import _process_single_pdf, _process_single_md
from ecs_quantitative.core.hardware import compute_sha256

PDF_NAME = "modelo_proyecto-1.pdf"
PDF_PATH = VAULT_DIR / PDF_NAME
OUTPUT_MD = PDF_PATH.with_suffix(".md")

def main():
    print(f"🚀 Iniciando Ingesta Soberana (High-Fidelity) para: {PDF_NAME}")
    
    if not PDF_PATH.exists():
        print(f"❌ Error: No se encuentra el archivo {PDF_PATH}")
        return

    # 1. Extracción PDF -> Markdown (Capa Intermedia)
    # Usamos el extractor nativo de PyMuPDF (fitz) por defecto vía _process_single_pdf
    print("  [1/2] Extrayendo contenido PDF...")
    success_pdf = _process_single_pdf(
        pdf_path=PDF_PATH,
        raw_dir=VAULT_DIR,
        output_dir=VAULT_DIR,
        char_threshold=100, 
        force=True,
        source_hash=compute_sha256(PDF_PATH)
    )
    
    if not success_pdf:
        print("❌ Error en la extracción del PDF.")
        return

    # 2. Sanitización Académica (Pipeline USP)
    print("  [2/2] Aplicando Sanitización Académica (USP)...")
    # _process_single_md sanitiza el archivo .md generado y lo guarda en output_dir
    # Como output_dir = VAULT_DIR y el archivo ya está ahí, se sanitiza in-place.
    success_sanit = _process_single_md(
        md_file=OUTPUT_MD,
        output_dir=VAULT_DIR,
        force=True
    )
    
    if success_sanit:
        print(f"✅ Proceso completado con éxito.")
        print(f"📄 Resultado: {OUTPUT_MD.relative_to(PROJECT_ROOT)}")
    else:
        print("⚠️ El archivo se extrajo pero la sanitización reportó problemas o no fue necesaria.")

if __name__ == "__main__":
    main()
