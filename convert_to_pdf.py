#!/usr/bin/env python3
"""
📄 CONVERTIR IMÁGENES A PDF
🔧 Convierte las imágenes descargadas a PDFs
"""

import os
import logging
from pathlib import Path
from manga_downloader_edge import EdgeMangaDownloader

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_chapters_to_pdf():
    """Convertir capítulos descargados a PDF"""
    
    print("📄 CONVERSOR DE IMÁGENES A PDF")
    print("=" * 50)
    
    downloads_dir = Path("downloads")
    
    if not downloads_dir.exists():
        print("❌ No existe el directorio downloads")
        return
    
    # Buscar directorios de capítulos
    chapter_dirs = list(downloads_dir.glob("capitulo_*"))
    
    if not chapter_dirs:
        print("❌ No se encontraron directorios de capítulos")
        return
    
    print(f"📁 Encontrados {len(chapter_dirs)} directorios de capítulos:")
    for chapter_dir in sorted(chapter_dirs):
        images = list(chapter_dir.glob("pagina_*.webp"))
        print(f"   📖 {chapter_dir.name}: {len(images)} imágenes")
    
    # Crear downloader
    downloader = EdgeMangaDownloader()
    
    # Crear directorio de PDFs
    pdf_dir = downloads_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)
    
    converted = 0
    for chapter_dir in sorted(chapter_dirs):
        try:
            # Extraer número de capítulo
            chapter_num = int(chapter_dir.name.split('_')[1])
            
            # Buscar imágenes
            image_files = sorted(chapter_dir.glob("pagina_*.webp"))
            
            if not image_files:
                print(f"⚠️ No hay imágenes en {chapter_dir.name}")
                continue
            
            print(f"\n📄 Convirtiendo capítulo {chapter_num} ({len(image_files)} imágenes)...")
            
            # Convertir paths a strings
            image_paths = [str(img) for img in image_files]
            
            # Crear PDF usando el método del downloader
            pdf_path = downloader.images_to_pdf(image_paths, chapter_num)
            
            if pdf_path:
                print(f"✅ PDF creado: {pdf_path}")
                converted += 1
            else:
                print(f"❌ Error creando PDF para capítulo {chapter_num}")
                
        except Exception as e:
            print(f"❌ Error procesando {chapter_dir.name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 RESUMEN:")
    print(f"   📁 Directorios procesados: {len(chapter_dirs)}")
    print(f"   ✅ PDFs creados: {converted}")
    print(f"   ❌ Errores: {len(chapter_dirs) - converted}")
    
    if converted > 0:
        print(f"\n📁 PDFs guardados en: {pdf_dir}")
        
        # Listar PDFs creados
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if pdf_files:
            print(f"📄 Archivos PDF:")
            for pdf_file in sorted(pdf_files):
                size_mb = pdf_file.stat().st_size / (1024 * 1024)
                print(f"   📖 {pdf_file.name} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    convert_chapters_to_pdf()