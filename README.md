# Descargador de Manga Bato.to

Una aplicación completa para descargar mangas de Bato.to y convertirlos a PDF.

## 🚀 Características

- ✅ Descarga todos los capítulos de un manga automáticamente
- ✅ Cambia automáticamente al modo "All Pages" para ver todas las imágenes
- ✅ Descarga todas las imágenes de cada capítulo
- ✅ Crea PDFs individuales por capítulo
- ✅ Genera un PDF unificado con todos los capítulos
- ✅ Manejo robusto de errores y reintentos
- ✅ Logging detallado del proceso

## 📋 Requisitos Previos

- Python 3.7 o superior
- Google Chrome instalado
- Conexión a internet estable

## 🛠️ Instalación

1. **Clonar o descargar los archivos**
2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar ChromeDriver:**
   ```bash
   python setup_chromedriver.py
   ```

## 🎯 Uso

### Descarga Simple
```bash
python manga_downloader.py
```

### Configuración Personalizada
Edita las siguientes variables en `manga_downloader.py`:
```python
manga_url = "https://bato.to/title/141482-demon-king-x-adventurer"
download_dir = "downloads/demon_king_x_adventurer"
```

## 📁 Estructura de Archivos

```
downloads/demon_king_x_adventurer/
├── capitulo_1/
│   ├── pagina_001.webp
│   ├── pagina_002.webp
│   └── ...
├── capitulo_2/
│   └── ...
├── pdfs/
│   ├── capitulo_1.pdf
│   ├── capitulo_2.pdf
│   └── ...
├── demon_king_x_adventurer_completo.pdf
└── manga_downloader.log
```

## ⚙️ Configuración Avanzada

### Modo Headless
Por defecto, el navegador ejecuta en modo headless (sin ventana visible). Para ver el proceso:
```python
chrome_options.add_argument('--headless')  # Comentar esta línea
```

### Timeout y Reintentos
Ajustar los tiempos de espera en el código:
```python
time.sleep(3)  # Tiempo entre acciones
timeout=30     # Timeout para descargas
```

### User Agent
El script usa un User Agent moderno para evitar detección:
```python
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...'
```

## 🔧 Solución de Problemas

### Error: ChromeDriver no encontrado
```bash
python setup_chromedriver.py
```

### Error: Timeout en descarga
- Verificar conexión a internet
- Aumentar valores de timeout en el código
- Ejecutar en horarios de menor tráfico

### Error: No se encuentran capítulos
- Verificar que la URL del manga sea correcta
- Comprobar que el manga esté disponible en Bato.to
- Revisar el log para más detalles

### Error: Memoria insuficiente
- Procesar capítulos individualmente
- Reducir calidad de imágenes antes de convertir a PDF
- Cerrar otras aplicaciones

## 📊 Logging

El script genera logs detallados en:
- `manga_downloader.log` - Archivo de log
- Consola - Output en tiempo real

Niveles de log:
- `INFO` - Información general del proceso
- `WARNING` - Advertencias no críticas
- `ERROR` - Errores que impiden la descarga

## 🚨 Consideraciones Legales

- ✅ Usar solo para contenido legal y gratuito
- ✅ Respetar los términos de servicio de Bato.to
- ✅ No redistribuir contenido con derechos de autor
- ✅ Usar con moderación para no sobrecargar el servidor

## 🤝 Contribuciones

Las mejoras son bienvenidas:
- Optimización de rendimiento
- Mejor manejo de errores
- Soporte para otros sitios de manga
- Interfaz gráfica de usuario

## 📝 Notas Técnicas

### Selenium WebDriver
- Usa Chrome en modo headless
- Maneja JavaScript dinámico
- Simula interacción de usuario real

### Gestión de Imágenes
- Descarga imágenes en formato original
- Convierte a RGB para PDF
- Mantiene calidad original

### Generación de PDF
- Usa ReportLab para crear PDFs
- Ajusta tamaño de página a cada imagen
- Combina múltiples PDFs eficientemente

## 📞 Soporte

Si encuentras problemas:
1. Revisa el archivo de log
2. Verifica la configuración de ChromeDriver
3. Comprueba la conectividad a internet
4. Asegúrate de que la URL del manga sea válida

---

**¡Disfruta leyendo tus mangas en PDF! 📚✨**