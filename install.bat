@echo off
echo ==========================================
echo    Instalador de Manga Downloader
echo ==========================================
echo.

echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Por favor instala Python 3.7 o superior.
    echo 💡 Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo 📦 Instalando dependencias de Python...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo 🔧 Configurando ChromeDriver...
python setup_chromedriver.py
if errorlevel 1 (
    echo ⚠️ Problema con ChromeDriver, pero continuando...
)

echo.
echo ==========================================
echo    Instalación Completada! 🎉
echo ==========================================
echo.
echo 🎯 Para usar el descargador:
echo    python manga_downloader.py
echo.
echo 📚 Para más información:
echo    README.md
echo.
pause