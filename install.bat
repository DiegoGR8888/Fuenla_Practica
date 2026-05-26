@echo off
REM Script de instalación automática para Fuenlabrada Smart Priorities
REM Compatible con Windows

echo ========================================
echo Fuenlabrada Smart Priorities - Installer
echo ========================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    echo Descarga Python desde https://www.python.org/
    echo Asegúrate de marcar "Add Python to PATH"
    pause
    exit /b 1
)

echo Python detectado: 
python --version
echo.

REM Crear entorno virtual
echo [1/4] Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo [3/4] Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo [4/4] Instalando dependencias...
pip install -r requirements.txt

REM Mensaje de éxito
echo.
echo ========================================
echo INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para iniciar la aplicación, ejecuta:
echo.
echo   streamlit run app.py
echo.
echo O ejecuta el script run.bat que encontrarás en esta carpeta
echo.
pause
