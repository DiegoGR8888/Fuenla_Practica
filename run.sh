#!/bin/bash
# Script para ejecutar Fuenlabrada Smart Priorities
# Compatible con macOS y Linux

echo "========================================"
echo "Fuenlabrada Smart Priorities"
echo "========================================"
echo ""

# Activar entorno virtual
source venv/bin/activate

# Verificar que el entorno está activado
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo activar el entorno virtual"
    echo "Asegúrate de haber ejecutado install.sh primero"
    exit 1
fi

# Ejecutar Streamlit
echo "Iniciando aplicación..."
echo "La aplicación se abrirá en http://localhost:8501"
echo ""
echo "Presiona Ctrl+C para detener"
echo ""

streamlit run app.py

# Si hay error
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: No se pudo iniciar la aplicación"
    echo "Verifica que todas las dependencias están instaladas"
fi
