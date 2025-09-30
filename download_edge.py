#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 DESCARGADOR DE MANGAS ULTRA RÁPIDO - VERSIÓN MICROSOFT EDGE
==============================================================

Características ULTRA RÁPIDAS con Edge:
✅ Usa tu perfil real de Microsoft Edge (sin conflictos)
✅ Motor Chromium pero más estable para automatización  
✅ Sin problemas de Chrome en uso
✅ Descargas paralelas ultra rápidas (8 hilos)
✅ Detección perfecta de imágenes con JavaScript
✅ Ancho uniforme preservando contenido
✅ Portada automática incluida

Compatible con: bato.to y xbato.com
"""

import sys
import os
import time
from manga_downloader_edge import EdgeMangaDownloader

def print_banner():
    """Mostrar banner del programa"""
    print("\n" + "="*60)
    print("🚀 DESCARGADOR ULTRA RÁPIDO DE MANGAS - EDGE EDITION")
    print("🌐 Compatible con: bato.to y xbato.com")
    print("="*60)

def get_manga_info(url):
    """Extraer información básica del manga de la URL"""
    try:
        if 'bato.to' in url or 'xbato.com' in url:
            parts = url.rstrip('/').split('/')
            manga_id = parts[-1] if parts else 'unknown'
            manga_name = manga_id.replace('-', ' ').title()
            return manga_id, manga_name
        else:
            return 'unknown', 'Unknown Manga'
    except:
        return 'unknown', 'Unknown Manga'

def validate_url(url):
    """Validar que la URL sea compatible"""
    if not url:
        return False
    
    valid_domains = ['bato.to', 'xbato.com']
    return any(domain in url.lower() for domain in valid_domains)

def main():
    """Función principal"""
    try:
        print_banner()
        
        # Solicitar URL del manga
        print("\n📖 Ingresa la URL del manga de bato.to o xbato.com:")
        print("📋 Ejemplos:")
        print("   https://bato.to/title/141482-demon-king-x-adventurer")
        print("   https://xbato.com/title/186157-black-blood-official")
        
        manga_url = input("🔗 URL: ").strip()
        
        # Validar URL
        if not validate_url(manga_url):
            print("❌ ERROR: URL no válida. Debe ser de bato.to o xbato.com")
            return
        
        # Obtener información del manga
        manga_id, manga_name = get_manga_info(manga_url)
        
        # Configuración de descarga
        print(f"\n⚙️ Configuración de Descarga:")
        download_all = input("¿Quieres descargar todos los capítulos? (S/n): ").strip().lower()
        
        start_chapter = 1
        end_chapter = None
        
        if download_all not in ['s', 'si', 'sí', 'yes', 'y', '']:
            try:
                start_chapter = int(input("📖 Capítulo inicial (por defecto 1): ") or "1")
                end_input = input("📖 Capítulo final (Enter para todos): ").strip()
                if end_input:
                    end_chapter = int(end_input)
            except ValueError:
                print("⚠️ Números inválidos, usando valores por defecto")
                start_chapter = 1
                end_chapter = None
        
        # Mostrar información del manga
        print(f"\n🎌 Información del Manga")
        print("="*50)
        print(f"📖 URL: {manga_url}")
        print(f"🆔 ID: {manga_id}")
        print(f"📚 Nombre: {manga_name}")
        print(f"📁 Directorio: downloads/{manga_id}")
        
        if end_chapter:
            print(f"📖 Capítulos: {start_chapter} - {end_chapter}")
        else:
            print(f"📖 Capítulos: {start_chapter} en adelante")
        
        # Confirmar descarga
        print(f"\n🚀 Iniciando descarga con Microsoft Edge...")
        
        # Crear descargador y ejecutar
        downloader = EdgeMangaDownloader()
        
        try:
            success = downloader.download_manga(
                manga_url=manga_url,
                start_chapter=start_chapter,
                end_chapter=end_chapter
            )
            
            if success:
                print(f"\n{'='*50}")
                print("🎉 ¡DESCARGA COMPLETADA!")
                print(f"📁 Directorio: downloads/{manga_id}")
                print(f"{'='*50}")
            else:
                print(f"\n❌ Error durante la descarga")
                
        finally:
            downloader.cleanup()
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Descarga cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
    finally:
        input("\n📝 Presiona Enter para salir...")

if __name__ == "__main__":
    # Configurar codificación para Windows
    if sys.platform.startswith('win'):
        import locale
        try:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
            except:
                pass
    
    main()