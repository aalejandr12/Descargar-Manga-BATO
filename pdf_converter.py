#!/usr/bin/env python3
"""
📄 CONVERSOR SIMPLE A PDF
🔧 Convierte imágenes WebP a PDF directamente
"""

import os
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io

def convert_images_to_pdf_simple(chapter_num, image_files, output_dir):
    """Convertir imágenes a PDF usando método simple"""
    
    if not image_files:
        print(f"❌ No hay imágenes para capítulo {chapter_num}")
        return None
    
    # Crear path de salida
    output_path = output_dir / f"capitulo_{chapter_num:03d}.pdf"
    
    print(f"📄 Creando PDF: {output_path}")
    
    try:
        # Crear canvas PDF
        c = canvas.Canvas(str(output_path))
        
        for i, image_file in enumerate(image_files, 1):
            try:
                # Abrir imagen
                with Image.open(image_file) as img:
                    # Convertir a RGB si es necesario
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Obtener dimensiones
                    width, height = img.size
                    
                    # Calcular escala para ajustar a página
                    page_width = 595  # A4 width en puntos
                    page_height = 842  # A4 height en puntos
                    
                    scale_x = page_width / width
                    scale_y = page_height / height
                    scale = min(scale_x, scale_y)  # Mantener proporciones
                    
                    new_width = width * scale
                    new_height = height * scale
                    
                    # Centrar en página
                    x = (page_width - new_width) / 2
                    y = (page_height - new_height) / 2
                    
                    # Convertir imagen a bytes
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='JPEG', quality=85)
                    img_buffer.seek(0)
                    
                    # Agregar imagen al PDF
                    c.setPageSize((page_width, page_height))
                    c.drawImage(ImageReader(img_buffer), x, y, width=new_width, height=new_height)
                    c.showPage()
                    
                    print(f"   ✅ Página {i}/{len(image_files)}: {Path(image_file).name}")
                    
            except Exception as e:
                print(f"   ❌ Error procesando {Path(image_file).name}: {e}")
                continue
        
        # Guardar PDF
        c.save()
        
        # Verificar tamaño
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"✅ PDF creado: {output_path.name} ({size_mb:.1f} MB)")
        
        return str(output_path)
        
    except Exception as e:
        print(f"❌ Error creando PDF: {e}")
        return None

def main():
    """Convertir todos los capítulos descargados"""
    
    print("📄 CONVERSOR SIMPLE A PDF")
    print("=" * 50)
    
    downloads_dir = Path("downloads")
    
    # Crear directorio PDFs
    pdf_dir = downloads_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)
    
    # Buscar directorios de capítulos
    chapter_dirs = sorted(downloads_dir.glob("capitulo_*"))
    
    if not chapter_dirs:
        print("❌ No se encontraron capítulos descargados")
        return
    
    print(f"📁 Encontrados {len(chapter_dirs)} capítulos:")
    
    converted = 0
    for chapter_dir in chapter_dirs:
        try:
            # Extraer número
            chapter_num = int(chapter_dir.name.split('_')[1])
            
            # Buscar imágenes
            image_files = sorted(chapter_dir.glob("pagina_*.webp"))
            
            print(f"\n📖 Capítulo {chapter_num}: {len(image_files)} imágenes")
            
            if not image_files:
                print("   ⚠️ Sin imágenes")
                continue
            
            # Convertir
            pdf_path = convert_images_to_pdf_simple(chapter_num, image_files, pdf_dir)
            
            if pdf_path:
                converted += 1
            
        except Exception as e:
            print(f"❌ Error con {chapter_dir.name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 RESUMEN FINAL:")
    print(f"   📁 Capítulos procesados: {len(chapter_dirs)}")
    print(f"   ✅ PDFs creados: {converted}")
    
    if converted > 0:
        print(f"\n📄 PDFs creados en: {pdf_dir}")
        
        # Listar archivos finales
        pdf_files = sorted(pdf_dir.glob("*.pdf"))
        total_size = 0
        
        for pdf_file in pdf_files:
            size_mb = pdf_file.stat().st_size / (1024 * 1024)
            total_size += size_mb
            print(f"   📖 {pdf_file.name} ({size_mb:.1f} MB)")
        
        print(f"\n💾 Tamaño total: {total_size:.1f} MB")

if __name__ == "__main__":
    main()