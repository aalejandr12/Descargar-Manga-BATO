import logging
import os
import re
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from typing import List, Optional
from urllib.parse import urlparse, urljoin
import PyPDF2

class EdgeMangaDownloader:
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = download_dir
        self.driver = None
        self.session = requests.Session()
        
        # Configurar logging sin emojis
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('manga_downloader.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Headers realistas
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def setup_edge_driver(self):
        """Configurar Microsoft Edge con perfil real"""
        try:
            edge_options = Options()
            
            # Configuraciones de rendimiento ULTRA RÁPIDAS
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')
            edge_options.add_argument('--disable-gpu')
            edge_options.add_argument('--disable-extensions')
            edge_options.add_argument('--disable-plugins')
            edge_options.add_argument('--disable-images')  # No cargar imágenes para velocidad
            edge_options.add_argument('--aggressive-cache-discard')
            edge_options.add_argument('--memory-pressure-off')
            edge_options.add_argument('--max-old-space-size=4096')
            
            # Usar perfil temporal inspirado en el real de Edge
            temp_profile = os.path.join(os.getcwd(), "edge_temp_profile")
            edge_options.add_argument(f'--user-data-dir={temp_profile}')
            edge_options.add_argument('--profile-directory=Default')
            self.logger.info("Usando perfil temporal para Microsoft Edge")
            
            # Configuraciones anti-detección
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)
            edge_options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Intentar con EdgeChromiumDriverManager primero, luego manual
            try:
                service = Service(EdgeChromiumDriverManager().install())
                self.logger.info("Driver descargado automáticamente")
            except:
                # Fallback: usar Edge instalado en el sistema
                edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe"
                if not os.path.exists(edge_path):
                    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedgedriver.exe"
                
                if os.path.exists(edge_path):
                    service = Service(edge_path)
                    self.logger.info("Usando driver de Edge del sistema")
                else:
                    # Último recurso: Edge sin service específico
                    service = None
                    self.logger.info("Intentando Edge sin service específico")
            
            if service:
                self.driver = webdriver.Edge(service=service, options=edge_options)
            else:
                self.driver = webdriver.Edge(options=edge_options)
            
            # Script anti-detección
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Driver de Microsoft Edge configurado exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error configurando Edge: {str(e)}")
            return False

    def get_chapters_list(self, manga_url: str) -> List[tuple]:
        """Obtener lista de capítulos"""
        try:
            self.logger.info(f"Obteniendo lista de capítulos de: {manga_url}")
            
            if not self.setup_edge_driver():
                return []
            
            self.driver.get(manga_url)
            time.sleep(3)
            
            # Buscar enlaces de capítulos con JavaScript
            chapter_script = """
            const chapters = [];
            const links = document.querySelectorAll('a[href*="/ch_"], a[href*="-ch_"], a[href*="chapter"]');
            
            links.forEach(link => {
                const href = link.href;
                const text = link.textContent.trim();
                if (href && text && (href.includes('/ch_') || href.includes('-ch_'))) {
                    chapters.push({
                        url: href,
                        title: text,
                        number: href.match(/ch_(\d+(?:\.\d+)?)/)?.[1] || chapters.length + 1
                    });
                }
            });
            
            return chapters;
            """
            
            chapters_data = self.driver.execute_script(chapter_script)
            
            if not chapters_data:
                self.logger.warning("No se encontraron capítulos con JavaScript, intentando con CSS")
                # Fallback con selectores CSS
                links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="ch_"], a[href*="-ch_"]')
                chapters_data = []
                for link in links:
                    href = link.get_attribute('href')
                    text = link.text.strip()
                    if href and text:
                        match = re.search(r'ch_(\d+(?:\.\d+)?)', href)
                        number = match.group(1) if match else len(chapters_data) + 1
                        chapters_data.append({
                            'url': href,
                            'title': text,
                            'number': number
                        })
            
            # Convertir a lista de tuplas y eliminar duplicados
            chapters = []
            seen_urls = set()
            
            for chapter in chapters_data:
                url = chapter['url']
                if url not in seen_urls:
                    seen_urls.add(url)
                    chapters.append((
                        float(chapter['number']) if isinstance(chapter['number'], str) else chapter['number'],
                        chapter['title'],
                        url
                    ))
            
            # Ordenar por número de capítulo
            chapters.sort(key=lambda x: x[0])
            
            self.logger.info(f"Enlaces encontrados: {len(chapters_data)}")
            self.logger.info(f"Capítulos encontrados: {len(chapters)}")
            
            return chapters
            
        except Exception as e:
            self.logger.error(f"Error obteniendo capítulos: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()

    def get_chapter_images(self, chapter_url: str) -> List[str]:
        """Obtener URLs de imágenes de un capítulo - OPTIMIZADO PARA EDGE"""
        try:
            if not self.setup_edge_driver():
                return []
            
            self.driver.get(chapter_url)
            time.sleep(5)  # Esperar carga
            
            # Script optimizado para encontrar imágenes
            image_script = """
            const images = [];
            
            // Prioridad 1: Buscar en div[name="image-items"] como mostraste
            const imageItems = document.querySelector('div[name="image-items"]');
            if (imageItems) {
                const imgs = imageItems.querySelectorAll('img[src]');
                imgs.forEach(img => {
                    if (img.src && !img.src.includes('data:')) {
                        images.push(img.src);
                    }
                });
            }
            
            // Prioridad 2: Buscar en contenedores comunes si no encontró nada
            if (images.length === 0) {
                const selectors = [
                    'div[name="image-item"] img',
                    '.chapter-images img',
                    '.reader img',
                    '.manga-reader img',
                    'img[src*="media"]',
                    'img[src*="chapter"]'
                ];
                
                for (const selector of selectors) {
                    const imgs = document.querySelectorAll(selector);
                    imgs.forEach(img => {
                        if (img.src && !img.src.includes('data:') && !images.includes(img.src)) {
                            images.push(img.src);
                        }
                    });
                    if (images.length > 0) break;
                }
            }
            
            return images.filter(url => url && url.length > 10);
            """
            
            image_urls = self.driver.execute_script(image_script)
            
            if not image_urls:
                self.logger.warning("JavaScript no encontró imágenes, intentando con Selenium")
                # Fallback con Selenium
                img_elements = self.driver.find_elements(By.CSS_SELECTOR, 'img[src]')
                image_urls = []
                for img in img_elements:
                    src = img.get_attribute('src')
                    if src and 'data:' not in src and len(src) > 10:
                        image_urls.append(src)
            
            # Filtrar y limpiar URLs
            filtered_urls = []
            for url in image_urls:
                if url and not any(skip in url.lower() for skip in ['avatar', 'logo', 'icon', 'banner']):
                    filtered_urls.append(url)
            
            self.logger.info(f"Encontradas {len(filtered_urls)} imágenes")
            return filtered_urls
            
        except Exception as e:
            self.logger.error(f"Error obteniendo imágenes: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()

    def download_single_image(self, url: str, filepath: str) -> bool:
        """Descargar una imagen individual con reintentos"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verificar que el archivo se descargó correctamente
                if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                    filename = os.path.basename(filepath)
                    self.logger.info(f"Descargada: {filename}")
                    return True
                
            except Exception as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"Reintento {attempt + 1} para {os.path.basename(filepath)}: {str(e)}")
                    time.sleep(2)
                else:
                    self.logger.error(f"Error descargando {os.path.basename(filepath)}: {str(e)}")
        
        return False

    def download_chapter_images(self, chapter_dir: str, image_urls: List[str]) -> List[str]:
        """Descargar imágenes de un capítulo en paralelo - ULTRA RÁPIDO"""
        os.makedirs(chapter_dir, exist_ok=True)
        downloaded_files = []
        
        def download_image_task(args):
            i, url = args
            extension = url.split('.')[-1].split('?')[0] if '.' in url else 'jpg'
            if extension not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                extension = 'jpg'
            
            filename = f"pagina_{i+1:03d}.{extension}"
            filepath = os.path.join(chapter_dir, filename)
            
            if self.download_single_image(url, filepath):
                return filepath
            return None
        
        # Usar más threads para Edge (es más estable)
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_url = {
                executor.submit(download_image_task, (i, url)): url 
                for i, url in enumerate(image_urls)
            }
            
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    downloaded_files.append(result)
        
        return sorted(downloaded_files)

    def get_cover_image(self, manga_url: str) -> Optional[str]:
        """Obtener imagen de portada del manga"""
        try:
            if not self.setup_edge_driver():
                return None
            
            self.logger.info("Extrayendo imagen de portada...")
            self.driver.get(manga_url)
            time.sleep(3)
            
            # Script para encontrar la portada
            cover_script = """
            const selectors = [
                'img[src*="thumb"]',
                '.manga-cover img',
                '.cover img',
                'img[src*="cover"]',
                '.thumbnail img',
                'img[alt*="cover"]'
            ];
            
            for (const selector of selectors) {
                const img = document.querySelector(selector);
                if (img && img.src && !img.src.includes('data:')) {
                    return img.src;
                }
            }
            return null;
            """
            
            cover_url = self.driver.execute_script(cover_script)
            
            if cover_url:
                self.logger.info(f"Imagen de portada encontrada: {cover_url}")
                return cover_url
            else:
                self.logger.warning("No se encontró imagen de portada")
                return None
                
        except Exception as e:
            self.logger.error(f"Error obteniendo portada: {str(e)}")
            return None
        finally:
            if self.driver:
                self.driver.quit()

    def download_cover_image(self, cover_url: str, manga_dir: str) -> Optional[str]:
        """Descargar imagen de portada"""
        try:
            self.logger.info("Descargando imagen de portada...")
            
            extension = cover_url.split('.')[-1].split('?')[0] if '.' in cover_url else 'jpg'
            if extension not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                extension = 'jpg'
            
            cover_path = os.path.join(manga_dir, f"portada.{extension}")
            
            if self.download_single_image(cover_url, cover_path):
                self.logger.info(f"Portada descargada: {cover_path}")
                return cover_path
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error descargando portada: {str(e)}")
            return None

    def images_to_pdf(self, image_files: List[str], output_path: str, cover_image: Optional[str] = None) -> bool:
        """Convertir imágenes a PDF con ancho uniforme"""
        try:
            if not image_files:
                self.logger.warning("No hay imágenes para convertir a PDF")
                return False
            
            # Crear lista de imágenes con portada al inicio si existe
            all_images = []
            if cover_image and os.path.exists(cover_image):
                all_images.append(cover_image)
                self.logger.info("Añadiendo portada al PDF")
            all_images.extend(image_files)
            
            # Analizar anchos para encontrar el ancho estándar
            widths = []
            for image_path in all_images:
                try:
                    with Image.open(image_path) as img:
                        widths.append(img.width)
                except:
                    continue
            
            if not widths:
                self.logger.error("No se pudieron analizar las imágenes")
                return False
            
            # Encontrar el ancho más común
            from collections import Counter
            width_counts = Counter(widths)
            target_width = width_counts.most_common(1)[0][0]
            
            self.logger.info(f"Ancho objetivo: {target_width}px (alto original mantenido)")
            
            # Crear PDF con ancho uniforme
            c = None
            
            for i, image_file in enumerate(all_images):
                try:
                    with Image.open(image_file) as img:
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        original_width, original_height = img.size
                        
                        # Solo redimensionar el ancho si es diferente
                        if original_width != target_width:
                            scale_factor = target_width / original_width
                            new_height = int(original_height * scale_factor)
                            img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
                        else:
                            new_height = original_height
                        
                        # Guardar imagen temporal
                        temp_path = f"temp_resized_{i}.jpg"
                        img.save(temp_path, "JPEG", quality=95)
                        
                        # Crear/configurar canvas
                        if c is None:
                            c = canvas.Canvas(output_path, pagesize=(target_width, new_height))
                        
                        c.setPageSize((target_width, new_height))
                        c.drawImage(temp_path, 0, 0, target_width, new_height)
                        c.showPage()
                        
                        # Limpiar archivo temporal
                        try:
                            os.remove(temp_path)
                        except:
                            pass
                    
                    if (i + 1) % 10 == 0:
                        self.logger.info(f"Procesadas {i + 1}/{len(all_images)} imágenes")
                        
                except Exception as e:
                    self.logger.error(f"Error procesando imagen {image_file}: {e}")
                    continue
            
            if c:
                c.save()
                self.logger.info(f"PDF creado: {output_path}")
                
                # Verificar tamaño del archivo
                pdf_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                self.logger.info(f"Tamaño del PDF: {pdf_size:.2f} MB")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error creando PDF: {str(e)}")
            return False

    def merge_pdfs(self, pdf_files: List[str], output_path: str) -> bool:
        """Combinar múltiples PDFs en uno solo"""
        try:
            self.logger.info(f"Combinando {len(pdf_files)} PDFs...")
            
            merger = PyPDF2.PdfMerger()
            
            for pdf_file in pdf_files:
                if os.path.exists(pdf_file):
                    merger.append(pdf_file)
                    self.logger.info(f"Añadido: {os.path.basename(pdf_file)}")
            
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            
            merger.close()
            
            # Verificar tamaño del archivo final
            if os.path.exists(output_path):
                final_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                self.logger.info(f"PDF unificado creado: {output_path} ({final_size:.2f} MB)")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error combinando PDFs: {str(e)}")
            return False

    def download_manga(self, manga_url: str, start_chapter: int = 1, end_chapter: int = None) -> bool:
        """Descargar manga completo - VERSIÓN EDGE ULTRA RÁPIDA"""
        try:
            start_time = time.time()
            
            # Extraer información del manga
            manga_id = manga_url.split('/')[-1] if '/' in manga_url else 'unknown'
            manga_name = manga_id.replace('-', ' ').title()
            
            manga_dir = os.path.join(self.download_dir, manga_id)
            pdfs_dir = os.path.join(manga_dir, "pdfs")
            os.makedirs(pdfs_dir, exist_ok=True)
            
            # Obtener imagen de portada
            cover_url = self.get_cover_image(manga_url)
            cover_path = None
            if cover_url:
                cover_path = self.download_cover_image(cover_url, manga_dir)
            
            # Obtener lista de capítulos
            chapters = self.get_chapters_list(manga_url)
            if not chapters:
                self.logger.error("No se pudieron obtener los capítulos")
                return False
            
            # Filtrar capítulos según rango
            if end_chapter:
                chapters = [ch for ch in chapters if start_chapter <= ch[0] <= end_chapter]
            else:
                chapters = [ch for ch in chapters if ch[0] >= start_chapter]
            
            self.logger.info(f"Capítulos a procesar: {len(chapters)}")
            
            pdf_files = []
            successful_chapters = 0
            
            # Procesar cada capítulo
            for i, (chapter_num, chapter_title, chapter_url) in enumerate(chapters, 1):
                chapter_start_time = time.time()
                self.logger.info(f"[{i}/{len(chapters)}] Procesando capítulo {chapter_num}: {chapter_title}")
                
                # Crear directorio del capítulo
                chapter_dir = os.path.join(manga_dir, f"capitulo_{chapter_num}")
                
                # Obtener imágenes del capítulo
                self.logger.info(f"Obteniendo imágenes del capítulo: {chapter_url}")
                image_urls = self.get_chapter_images(chapter_url)
                
                if not image_urls:
                    self.logger.warning(f"No se encontraron imágenes para el capítulo {chapter_num}")
                    continue
                
                # Descargar imágenes
                self.logger.info(f"Descargando {len(image_urls)} imágenes del capítulo {chapter_num}")
                downloaded_images = self.download_chapter_images(chapter_dir, image_urls)
                
                if not downloaded_images:
                    self.logger.warning(f"No se descargaron imágenes para el capítulo {chapter_num}")
                    continue
                
                # Crear PDF del capítulo
                pdf_filename = f"capitulo_{chapter_num}.pdf"
                pdf_path = os.path.join(pdfs_dir, pdf_filename)
                
                if self.images_to_pdf(downloaded_images, pdf_path, cover_path):
                    pdf_files.append(pdf_path)
                    successful_chapters += 1
                    
                    chapter_time = time.time() - chapter_start_time
                    self.logger.info(f"✅ Capítulo {chapter_num} completado en {chapter_time:.1f}s")
                else:
                    self.logger.error(f"❌ Error creando PDF del capítulo {chapter_num}")
            
            # Crear PDF unificado
            if pdf_files:
                unified_pdf = os.path.join(manga_dir, f"{manga_id}_completo.pdf")
                self.merge_pdfs(pdf_files, unified_pdf)
            
            # Estadísticas finales
            total_time = time.time() - start_time
            self.logger.info("=" * 50)
            self.logger.info("🎉 DESCARGA COMPLETADA CON EDGE")
            self.logger.info(f"📚 Capítulos procesados: {successful_chapters}/{len(chapters)}")
            self.logger.info(f"📄 PDFs individuales: {len(pdf_files)}")
            if pdf_files:
                self.logger.info(f"📁 PDF unificado: {unified_pdf}")
            self.logger.info(f"⏱️ Tiempo total: {total_time/60:.1f} minutos")
            self.logger.info("=" * 50)
            
            return successful_chapters > 0
            
        except Exception as e:
            self.logger.error(f"Error en descarga completa: {str(e)}")
            return False

    def cleanup(self):
        """Limpiar recursos"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.session.close()

    def combine_all_pdfs(self, manga_dir, manga_id):
        """Combinar TODOS los PDFs individuales en un archivo final"""
        try:
            pdf_dir = os.path.join(manga_dir, "pdfs")
            
            if not os.path.exists(pdf_dir):
                self.logger.error("❌ Directorio de PDFs no encontrado")
                return False
            
            # Obtener todos los PDFs individuales
            pdf_files = []
            for file in os.listdir(pdf_dir):
                if file.startswith('capitulo_') and file.endswith('.pdf'):
                    pdf_files.append(os.path.join(pdf_dir, file))
            
            if not pdf_files:
                self.logger.error("❌ No se encontraron PDFs individuales para combinar")
                return False
            
            # Ordenar PDFs por número de capítulo
            def extract_chapter_number(filename):
                try:
                    base_name = os.path.basename(filename)
                    chapter_part = base_name.replace('capitulo_', '').replace('.pdf', '')
                    return float(chapter_part)
                except:
                    return 0
            
            pdf_files.sort(key=extract_chapter_number)
            
            self.logger.info(f"🔄 Combinando {len(pdf_files)} PDFs...")
            
            # Crear PDF unificado usando el método existente
            output_path = os.path.join(manga_dir, f"{manga_id}_completo.pdf")
            
            success = self.merge_pdfs(pdf_files, output_path)
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                file_size_mb = file_size / (1024 * 1024)
                
                self.logger.info(f"🎉 PDF COMPLETO REGENERADO: {output_path}")
                self.logger.info(f"📊 Tamaño: {file_size_mb:.2f} MB")
                self.logger.info(f"📚 Capítulos incluidos: {len(pdf_files)}")
                
                return True
            else:
                self.logger.error("❌ Error: El archivo PDF no se creó correctamente")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error combinando PDFs: {str(e)}")
            return False