#!/usr/bin/env python3
"""
High-Fidelity Vault Ingestion Script
Version: 8.1.5 (Intelligent Ecosystem)

Este script utiliza la librería central 'ecs_quantitative' para extraer y sanitizar
la documentación bibliográfica de la bóveda de Carigán.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Configuración de rutas
VAULT_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = VAULT_DIR.parent.parent.parent
LIB_ROOT = Path("/home/erick-fcs/Capital_Workstation/capital-workstation-libs/src")

if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.append(str(PROJECT_ROOT / "src"))
if str(LIB_ROOT) not in sys.path:
    sys.path.append(str(LIB_ROOT))

from ecs_quantitative.management.intelligence import (
    PDFToMarkdownConverter,
    BibliographicSanitizer,
)


def main():
    print("🚀 Iniciando Ingesta Soberana de la Bóveda (Carigán)")
    
    raw_dir = VAULT_DIR / "readings" / "raw"
    sanitized_dir = VAULT_DIR / "readings" / "sanitized"
    
    if not raw_dir.exists():
        print(f"❌ Error: La carpeta de origen {raw_dir} no existe.")
        return

    sanitized_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Conversión de PDF a Markdown (Capa Intermedia en Bóveda)
    print("  [1/2] Convirtiendo PDFs a Markdown...")
    converter = PDFToMarkdownConverter(raw_dir=raw_dir, output_dir=sanitized_dir)
    converted_count = converter.convert_all(force=True)
    print(f"  ✨ {converted_count} archivos convertidos a Markdown.")

    # 2. Sanitización Académica (USP Pipeline)
    print("  [2/2] Aplicando Sanitización Académica (USP)...")
    sanitizer = BibliographicSanitizer(input_dir=sanitized_dir, output_dir=sanitized_dir)
    sanitized_count = sanitizer.sanitize_all(force=True)
    print(f"  ✨ {sanitized_count} archivos sanitizados académicamente.")
    
    print("✅ Ingesta soberana completada con éxito.")


if __name__ == "__main__":
    main()
