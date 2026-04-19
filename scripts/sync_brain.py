import sys
import asyncio
from pathlib import Path

# Asegurar descubrimiento de src y librerías externas
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

LIBS_PATH = Path("/home/erick-fcs/Capital_Workstation/capital-workstation-libs")
if str(LIBS_PATH) not in sys.path:
    sys.path.append(str(LIBS_PATH))

from src.core.lineage import lineage_engine
from src.core.brain import LaboratorioBrain

try:
    from ecs_quantitative.ingestion.processors.pdf import PDFProcessor
except ImportError:
    PDFProcessor = None


async def sync_knowledge():
    print("🧠 Sincronizador de Conocimiento LPI v5.0")
    print("=" * 50)

    if not PDFProcessor:
        print("❌ Error: No se pudo cargar el procesador de PDFs.")
        return

    # 1. Obtener solo archivos verificados por el sistema de Linaje (Nivel 4)
    verified_files = lineage_engine.get_verified_files()

    if not verified_files:
        print("⚠️ No hay archivos verificados nuevos para indexar.")
        return

    print(f"📡 Detectados {len(verified_files)} archivos íntegros para el Cerebro.")

    # 2. Inicializar cerebro y procesador
    brain = LaboratorioBrain()
    processor = PDFProcessor(
        ocr_enabled=False
    )  # OCR desactivado por defecto por velocidad

    for f_info in verified_files:
        pdf_path = f_info["full_path"]
        print(f"📖 Aprendiendo de: {f_info['name']}...")

        # Extraer texto
        text, _ = await processor.extract_text(pdf_path)

        # Segmentación simple por párrafos (Mejorable en Nivel 6)
        chunks = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 50]

        print(f"   -> Generando {len(chunks)} fragmentos de conocimiento.")

        # Guardar en memoria
        for idx, chunk in enumerate(chunks):
            meta = {
                "source_id": f_info["id"],
                "source_name": f_info["name"],
                "verified": True,
                "type": "normative",
            }
            brain.memory.store(
                content=chunk, metadata=meta, doc_id=f"{f_info['id']}_v5_{idx}"
            )

    print("\n" + "=" * 50)
    print("✨ ÉXITO: El Cerebro del laboratorio ha sido actualizado y sincronizado.")


if __name__ == "__main__":
    asyncio.run(sync_knowledge())
