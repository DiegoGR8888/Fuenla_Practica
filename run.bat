@echo off
REM Script para ejecutar Fuenlabrada Smart Priorities
REM Compatible con Windows

echo ========================================
echo Fuenlabrada Smart Priorities
echo ========================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar que el entorno está activado
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    echo Asegúrate de haber ejecutado install.bat primero
    pause
    exit /b 1
)

REM Ejecutar Streamlit
echo Iniciando aplicación...
echo La aplicación se abrirá en http://localhost:8501
echo.
echo Presiona Ctrl+C para detener
echo.

streamlit run app.py

REM Si hay error
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo iniciar la aplicación
    echo Verifica que todas las dependencias están instaladas
    pause
)
