import asyncio
from pathlib import Path

from ecs_quantitative.ingestion.processors.pdf import PDFProcessor
from ecs_quantitative.memory.agent_memory import AgentMemory

# Infraestructura Federada
LIBS_SRC = Path("/home/erick-fcs/Capital_Workstation/capital-workstation-libs/src/ecs_quantitative")
PROJECT_ROOT = Path(__file__).parent.parent


async def sync_knowledge():
    print("🧠 Sincronizador de Conocimiento Federado v7.4.0")
    print("=" * 50)

    # 1. Auditar archivos locales para identificar fuentes válidas
    print(f"🔍 Auditando fuentes en {PROJECT_ROOT.name}...")

    # Simulación de recolección de PDFs del catálogo de datos (Simplificado para el Nodo Puro)
    # En una versión más avanzada, AuditEngine podría retornar el catálogo verificado
    sources_dir = PROJECT_ROOT / "data" / "raw" / "marco_normativo"
    pdf_files = list(sources_dir.glob("*.pdf"))

    if not pdf_files:
        print("⚠️ No se encontraron PDFs en data/raw/marco_normativo para indexar.")
        return

    print(f"📡 Detectados {len(pdf_files)} archivos para el Cerebro Central.")

    # 2. Inicializar componentes centrales
    memory = AgentMemory(collection_name="marco_normativo")
    processor = PDFProcessor(ocr_enabled=False)

    for pdf_path in pdf_files:
        source_id = pdf_path.stem
        print(f"📖 Aprendiendo de: {pdf_path.name}...")

        # --- CAPA DE SEGURIDAD: Evitar Duplicados ---
        try:
            col = memory.client.get_collection(name="marco_normativo")
            col.delete(where={"source_id": source_id})
        except Exception:
            pass
        # --------------------------------------------

        # Extraer texto usando el procesador centralizado
        text, _ = await processor.extract_text(str(pdf_path))

        # Segmentación (En el futuro, esto debería ser un método de PDFProcessor o TextSplitter)
        chunks = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 50]
        print(f"   -> Generando {len(chunks)} fragmentos de conocimiento federado.")

        # Guardar en memoria central
        for idx, chunk in enumerate(chunks):
            meta = {
                "source_id": source_id,
                "source_name": pdf_path.name,
                "project": PROJECT_ROOT.name,
                "type": "normative",
            }
            memory.store(
                content=chunk,
                metadata=meta,
                doc_id=f"{source_id}_{idx}",
                collection="marco_normativo",
            )

    print("\n" + "=" * 50)
    print("✨ ÉXITO: El Cerebro Central ha sido actualizado con conocimiento del nodo.")


if __name__ == "__main__":
    asyncio.run(sync_knowledge())
