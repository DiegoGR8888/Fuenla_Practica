#!/usr/bin/env python
"""
Script de Validación - Fuenlabrada Smart Priorities
Verifica que todo esté configurado correctamente
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica versión de Python"""
    print("✓ Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} (Se requiere 3.9+)")
        return False

def check_required_files():
    """Verifica archivos necesarios"""
    print("\n✓ Verificando archivos del proyecto...")
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "src/__init__.py",
        "src/data_loader.py",
        "src/cleaning.py",
        "src/indicators.py",
        "src/model.py",
        "src/maps.py",
        "src/recommendations.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (FALTA)")
            all_exist = False
    
    return all_exist

def check_packages():
    """Verifica dependencias instaladas"""
    print("\n✓ Verificando dependencias instaladas...")
    required_packages = {
        "streamlit": ">=1.28.0",
        "pandas": ">=2.1.0",
        "numpy": ">=1.26.0",
        "plotly": ">=5.17.0",
        "sklearn": ">=1.4.0",  # Note: scikit-learn se importa como sklearn
        "folium": ">=0.14.0",
        "streamlit_folium": ">=0.15.0",
        "requests": ">=2.31.0",
        "openpyxl": ">=3.1.0",
    }
    
    all_installed = True
    for package, version in required_packages.items():
        try:
            __import__(package)
            display_name = "scikit-learn" if package == "sklearn" else package.replace("_", "-")
            print(f"  ✅ {display_name} {version}")
        except ImportError:
            display_name = "scikit-learn" if package == "sklearn" else package.replace("_", "-")
            print(f"  ❌ {display_name} {version} (NO INSTALADO)")
            all_installed = False
    
    return all_installed

def check_data_files():
    """Verifica archivos de datos"""
    print("\n✓ Verificando estructura de datos...")
    data_dirs = [
        "data",
        "data/raw",
        "data/processed",
        "notebooks",
    ]
    
    for dir_path in data_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ⚠️  {dir_path}/ (Será creada automáticamente)")

def check_imports():
    """Verifica que los módulos se pueden importar"""
    print("\n✓ Verificando importación de módulos...")
    
    try:
        from src.data_loader import load_uploaded_file, create_sample_data
        print("  ✅ src.data_loader")
    except Exception as e:
        print(f"  ❌ src.data_loader ({str(e)})")
        return False
    
    try:
        from src.cleaning import normalize_columns, clean_numeric_data
        print("  ✅ src.cleaning")
    except Exception as e:
        print(f"  ❌ src.cleaning ({str(e)})")
        return False
    
    try:
        from src.indicators import calculate_urban_priority_index
        print("  ✅ src.indicators")
    except Exception as e:
        print(f"  ❌ src.indicators ({str(e)})")
        return False
    
    try:
        from src.model import PriorityPredictor
        print("  ✅ src.model")
    except Exception as e:
        print(f"  ❌ src.model ({str(e)})")
        return False
    
    try:
        from src.maps import create_folium_map
        print("  ✅ src.maps")
    except Exception as e:
        print(f"  ❌ src.maps ({str(e)})")
        return False
    
    try:
        from src.recommendations import RecommendationEngine
        print("  ✅ src.recommendations")
    except Exception as e:
        print(f"  ❌ src.recommendations ({str(e)})")
        return False
    
    return True

def main():
    """Función principal"""
    print("=" * 60)
    print("VALIDACIÓN DE CONFIGURACIÓN")
    print("Fuenlabrada Smart Priorities")
    print("=" * 60)
    
    results = {
        "Python": check_python_version(),
        "Archivos": check_required_files(),
        "Paquetes": check_packages(),
        "Módulos": check_imports(),
    }
    
    check_data_files()
    
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    for check, result in results.items():
        status = "✅ OK" if result else "❌ FALTA"
        print(f"{check}: {status}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n🎉 ¡TODO OK! La aplicación está lista para ejecutar:")
        print("\n   streamlit run app.py")
        return 0
    else:
        print("\n⚠️  Hay problemas de configuración.")
        print("\nSoluciona los errores marcados con ❌:")
        print("1. Instala los paquetes faltantes:")
        print("   pip install -r requirements.txt")
        print("2. Descarga los archivos faltantes del repositorio")
        print("3. Verifica que estás en la carpeta correcta")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
