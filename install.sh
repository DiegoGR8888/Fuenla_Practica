#!/bin/bash
# Script de instalación automática para Fuenlabrada Smart Priorities
# Compatible con macOS y Linux

echo "========================================"
echo "Fuenlabrada Smart Priorities - Installer"
echo "========================================"
echo ""

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "En macOS: brew install python3"
    echo "En Ubuntu: sudo apt-get install python3"
    exit 1
fi

echo "Python detectado:"
python3 --version
echo ""

# Crear entorno virtual
echo "[1/4] Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "[2/4] Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "[3/4] Actualizando pip..."
python3 -m pip install --upgrade pip

# Instalar dependencias
echo "[4/4] Instalando dependencias..."
pip install -r requirements.txt

# Mensaje de éxito
echo ""
echo "========================================"
echo "INSTALACIÓN COMPLETADA EXITOSAMENTE"
echo "========================================"
echo ""
echo "Para iniciar la aplicación, ejecuta:"
echo ""
echo "  streamlit run app.py"
echo ""
echo "O ejecuta el script run.sh que encontrarás en esta carpeta"
echo ""
