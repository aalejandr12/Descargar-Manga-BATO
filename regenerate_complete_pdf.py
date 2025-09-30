#!/usr/bin/env python3
"""
Regenerador de PDF Completo
Combina todos los PDFs individuales existentes en un archivo final
"""

import os
import sys
import logging
from manga_downloader_edge import EdgeMangaDownloader

def setup_logging():
    """Configurar logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def main():
    logger = setup_logging()
    
    print("=" * 60)
    print("📚 REGENERADOR DE PDF COMPLETO")
    print("🔄 Combina todos los capítulos existentes en un PDF final")
    print("=" * 60)
    
    # Configuración
    manga_id = "157079-i-want-to-be-an-incubus-too-mochiyen"
    base_dir = "downloads"
    manga_dir = os.path.join(base_dir, manga_id)
    pdf_dir = os.path.join(manga_dir, "pdfs")
    
    if not os.path.exists(pdf_dir):
        logger.error("❌ Directorio de PDFs no encontrado")
        return
    
    # Contar PDFs existentes
    pdf_files = []
    for file in os.listdir(pdf_dir):
        if file.startswith('capitulo_') and file.endswith('.pdf'):
            pdf_files.append(file)
    
    if not pdf_files:
        logger.error("❌ No se encontraron PDFs individuales")
        return
    
    logger.info(f"📁 Encontrados {len(pdf_files)} PDFs individuales")
    
    # Mostrar lista de capítulos
    chapter_numbers = []
    for file in pdf_files:
        try:
            chapter_part = file.replace('capitulo_', '').replace('.pdf', '')
            chapter_num = float(chapter_part)
            chapter_numbers.append(int(chapter_num) if chapter_num.is_integer() else chapter_num)
        except:
            continue
    
    chapter_numbers.sort()
    logger.info(f"📚 Capítulos disponibles: {chapter_numbers}")
    
    # Preguntar confirmación
    print(f"\n¿Regenerar PDF completo con {len(pdf_files)} capítulos? (S/n): ", end="")
    respuesta = input().strip().lower()
    
    if respuesta == 'n':
        print("❌ Regeneración cancelada")
        return
    
    # Crear el descargador solo para usar el método de combinación
    downloader = EdgeMangaDownloader()
    
    logger.info("🔄 Regenerando PDF completo...")
    
    try:
        success = downloader.combine_all_pdfs(manga_dir, manga_id)
        
        if success:
            final_pdf = os.path.join(manga_dir, f"{manga_id}_completo.pdf")
            if os.path.exists(final_pdf):
                file_size = os.path.getsize(final_pdf) / (1024 * 1024)
                
                print("\n" + "=" * 60)
                print("🎉 ¡PDF COMPLETO REGENERADO EXITOSAMENTE!")
                print(f"📁 Archivo: {final_pdf}")
                print(f"📊 Tamaño: {file_size:.2f} MB")
                print(f"📚 Capítulos incluidos: {len(pdf_files)}")
                print("=" * 60)
            else:
                logger.error("❌ Error: El archivo no se creó correctamente")
        else:
            logger.error("❌ Error al regenerar el PDF completo")
            
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
    
    finally:
        try:
            downloader.cleanup()
        except:
            pass

if __name__ == "__main__":
    main()