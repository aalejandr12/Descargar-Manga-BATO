# 📚 Descargador Universal de Mangas de Bato.to

## 🚀 Cómo Ejecutar la Aplicación

### 📋 **Métodos Disponibles**

#### **1. Descarga Automática (Demon King x Adventurer)**
Para el manga que ya configuramos:

```powershell
# Todos los capítulos
& ".venv/Scripts/python.exe" auto_download.py

# Solo 3 capítulos
& ".venv/Scripts/python.exe" auto_download.py 3

# Solo 1 capítulo para prueba
& ".venv/Scripts/python.exe" auto_download.py 1
```

#### **2. Descarga Universal (Cualquier manga de bato.to)**
```powershell
# Con cualquier URL de bato.to
& ".venv/Scripts/python.exe" download_any_manga.py "https://bato.to/title/12345-nombre-manga"

# Con límite de capítulos
& ".venv/Scripts/python.exe" download_any_manga.py "https://bato.to/title/12345-nombre-manga" --chapters 5

# Empezar desde un capítulo específico
& ".venv/Scripts/python.exe" download_any_manga.py "https://bato.to/title/12345-nombre-manga" --start 3 --chapters 10
```

#### **3. Modo Interactivo (Con preguntas)**
```powershell
& ".venv/Scripts/python.exe" manga_downloader_optimized.py
```
*Te preguntará la URL y configuraciones*

---

## 🔗 **Ejemplos de URLs Válidas**

```
https://bato.to/title/141482-demon-king-x-adventurer
https://bato.to/title/123456-otro-manga-ejemplo
https://bato.to/title/789012-manga-de-prueba
```

### ✅ **Formato Correcto:**
- Debe empezar con: `https://bato.to/title/`
- Formato: `https://bato.to/title/NÚMERO-nombre-del-manga`

---

## 📁 **Estructura de Archivos Generados**

```
downloads/
└── nombre-del-manga/
    ├── capitulo_1/           # Imágenes del capítulo 1
    │   ├── pagina_001.webp
    │   ├── pagina_002.webp
    │   └── ...
    ├── capitulo_2/           # Imágenes del capítulo 2
    │   └── ...
    ├── pdfs/                 # PDFs individuales
    │   ├── capitulo_1.pdf
    │   ├── capitulo_2.pdf
    │   └── ...
    └── nombre-manga_completo.pdf  # PDF unificado
```

---

## 🎯 **Ejemplos de Uso Completos**

### **Ejemplo 1: Manga Completo**
```powershell
& ".venv/Scripts/python.exe" download_any_manga.py "https://bato.to/title/141482-demon-king-x-adventurer"
```
*Descarga todos los capítulos disponibles*

### **Ejemplo 2: Solo Primeros 3 Capítulos**
```powershell
& ".venv/Scripts/python.exe" download_any_manga.py "https://bato.to/title/141482-demon-king-x-adventurer" --chapters 3
```

### **Ejemplo 3: Capítulos 5 al 10**
```powershell
& ".venv/Scripts/python.exe" download_any_manga.py "https://bato.to/title/141482-demon-king-x-adventurer" --start 5 --chapters 6
```
*Empezar en capítulo 5 y descargar 6 capítulos (del 5 al 10)*

### **Ejemplo 4: Otro Manga Completo**
```powershell
& ".venv/Scripts/python.exe" download_any_manga.py "https://bato.to/title/98765-mi-manga-favorito"
```

---

## ⚙️ **Opciones Avanzadas**

### **Parámetros del Descargador Universal:**
- `url`: URL del manga (requerido)
- `--chapters` o `-c`: Número máximo de capítulos
- `--start` o `-s`: Capítulo desde donde empezar

### **Ejemplos de Combinaciones:**
```powershell
# Últimos 5 capítulos (empezando desde el 15)
& ".venv/Scripts/python.exe" download_any_manga.py "URL_MANGA" --start 15 --chapters 5

# Solo el capítulo 1
& ".venv/Scripts/python.exe" download_any_manga.py "URL_MANGA" --chapters 1

# Desde el capítulo 10 hasta el final
& ".venv/Scripts/python.exe" download_any_manga.py "URL_MANGA" --start 10
```

---

## 📊 **Estadísticas de Rendimiento**
- **Velocidad**: ~30 segundos por capítulo (50+ imágenes)
- **Descarga Paralela**: Máximo 3 imágenes simultáneas
- **Formato**: PDFs de alta calidad con imágenes originales
- **Gestión de Errores**: Reintentos automáticos en caso de falla

---

## 🆘 **Solución de Problemas**

### **Error: "URL inválida"**
- Verifica que la URL comience con `https://bato.to/title/`
- Asegúrate de copiar la URL completa

### **Error: "No se encontraron capítulos"**
- El manga podría no estar disponible
- Verifica que la URL sea correcta
- Algunos mangas requieren login (no soportado actualmente)

### **Error de Chrome Driver**
- La aplicación descarga automáticamente el driver
- Si hay problemas, reinicia la aplicación

---

## 🎉 **¡Tu Aplicación está Lista!**

Ahora puedes descargar **cualquier manga de bato.to** usando estos comandos. La aplicación:

✅ Funciona con cualquier manga de bato.to  
✅ Detecta automáticamente todos los capítulos  
✅ Descarga en paralelo para mayor velocidad  
✅ Crea PDFs individuales y unificados  
✅ Gestiona errores automáticamente  
✅ Muestra progreso detallado