"""
Data Loader Module
Carga datos desde API CKAN de Fuenlabrada y archivos locales
"""

import pandas as pd
import numpy as np
import requests
import streamlit as st
from typing import Optional, Tuple


# URLs del API CKAN de Fuenlabrada
CKAN_API_URL = "https://data.fuenlabrada.es/api/3/action"

# Datasets públicos disponibles
DATASETS_MAPPING = {
    "Calidad del aire": "calidad-del-aire",
    "Contaminación acústica": "contaminacion-acustica",
    "Zonas verdes": "zonas-verdes",
    "Actividad comercial": "actividad-comercial",
    "Edificios públicos": "edificios-publicos",
    "Recursos sociales": "recursos-sociales",
    "Sanciones y multas": "sanciones-multas",
    "Transporte GTFS": "transporte-gtfs",
}


def get_datasets_from_api() -> dict:
    """
    Obtiene lista de datasets disponibles desde el API CKAN de Fuenlabrada
    
    Returns:
        dict: Diccionario con información de datasets disponibles
    """
    try:
        url = f"{CKAN_API_URL}/package_search"
        params = {"q": "fuenlabrada", "rows": 50}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("result", {})
        return {}
    except Exception as e:
        st.warning(f"Error al conectar con API CKAN: {str(e)}")
        return {}


def download_dataset_from_ckan(dataset_name: str) -> Optional[pd.DataFrame]:
    """
    Descarga un dataset específico del API CKAN
    
    Args:
        dataset_name: Nombre del dataset a descargar
        
    Returns:
        pd.DataFrame: Dataset descargado, o None si hay error
    """
    try:
        url = f"{CKAN_API_URL}/package_show"
        params = {"id": dataset_name}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            package = data.get("result", {})
            resources = package.get("resources", [])
            
            if resources:
                # Busca primer recurso CSV o XLSX
                download_url = None
                for resource in resources:
                    if resource.get("format", "").upper() in ["CSV", "XLSX", "XLS"]:
                        download_url = resource.get("url")
                        break
                
                if download_url:
                    if download_url.endswith(".xlsx") or download_url.endswith(".xls"):
                        df = pd.read_excel(download_url)
                    else:
                        df = pd.read_csv(download_url)
                    return df
        return None
    except Exception as e:
        st.warning(f"Error al descargar dataset {dataset_name}: {str(e)}")
        return None


def load_uploaded_file(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Carga un archivo subido (CSV o XLSX)
    
    Args:
        uploaded_file: Archivo subido en Streamlit
        
    Returns:
        pd.DataFrame: Datos cargados, o None si hay error
    """
    try:
        if uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            st.error("Formato no soportado. Usa CSV o XLSX")
            return None
        
        return df
    except Exception as e:
        st.error(f"Error al cargar archivo: {str(e)}")
        return None


def detect_zone_column(df: pd.DataFrame) -> Optional[str]:
    """
    Detecta automáticamente la columna de zona/barrio/distrito
    
    Args:
        df: DataFrame a analizar
        
    Returns:
        str: Nombre de la columna detectada, o None
    """
    zone_keywords = [
        "zona", "barrio", "distrito", "localidad", "sección", "area", 
        "neighborhood", "area_code", "district", "zone", "sector"
    ]
    
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in zone_keywords):
            return col
    
    return None


def detect_numeric_columns(df: pd.DataFrame) -> list:
    """
    Detecta columnas numéricas para análisis
    
    Args:
        df: DataFrame a analizar
        
    Returns:
        list: Lista de nombres de columnas numéricas
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()


def detect_geo_columns(df: pd.DataFrame) -> Tuple[Optional[str], Optional[str]]:
    """
    Detecta columnas de latitud y longitud
    
    Args:
        df: DataFrame a analizar
        
    Returns:
        Tuple: (columna_latitud, columna_longitud) o (None, None)
    """
    lat_keywords = ["lat", "latitude", "latitud", "y"]
    lon_keywords = ["lon", "long", "longitude", "longitud", "x"]
    
    lat_col = None
    lon_col = None
    
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in lat_keywords) and lat_col is None:
            lat_col = col
        if any(keyword in col_lower for keyword in lon_keywords) and lon_col is None:
            lon_col = col
    
    return lat_col, lon_col


def create_sample_data() -> pd.DataFrame:
    """
    Crea datos de muestra para Fuenlabrada para demostración
    
    Returns:
        pd.DataFrame: DataFrame con datos de muestra
    """
    np.random.seed(42)
    
    zones = [
        "Centro", "El Naranjo", "Loranca", "La Serna", "Arroyo-La Fuente",
        "Parque Miraflores", "Zona de Marañón", "Zona de la Estación",
        "Zona Industrial", "La Paz", "Los Ángeles", "Villaverde",
        "Fuencarral", "Fuenlabrada Este", "Fuenlabrada Oeste"
    ]
    
    data = {
        "zona": zones,
        "quejas": np.random.randint(50, 500, len(zones)),
        "contaminacion": np.random.uniform(30, 120, len(zones)),
        "ruido": np.random.uniform(55, 85, len(zones)),
        "zonas_verdes": np.random.uniform(5, 40, len(zones)),
        "servicios_publicos": np.random.randint(3, 20, len(zones)),
        "actividad_comercial": np.random.randint(20, 150, len(zones)),
        "poblacion": np.random.randint(5000, 50000, len(zones)),
        "latitud": np.random.uniform(40.30, 40.35, len(zones)),
        "longitud": np.random.uniform(-3.82, -3.78, len(zones)),
    }
    
    return pd.DataFrame(data).drop_duplicates(subset=["zona"]).reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_demo_datasets() -> dict:
    """
    Carga múltiples datasets de muestra para demostración
    
    Returns:
        dict: Diccionario con DataFrames para cada indicador
    """
    np.random.seed(42)
    zones = [
        "Centro", "El Naranjo", "Loranca", "La Serna", "Arroyo-La Fuente",
        "Parque Miraflores"
    ]
    
    datasets = {}
    
    # Dataset de calidad del aire
    datasets["aire"] = pd.DataFrame({
        "zona": zones,
        "PM10": np.random.uniform(30, 120, len(zones)),
        "PM25": np.random.uniform(15, 60, len(zones)),
        "NO2": np.random.uniform(20, 80, len(zones)),
        "O3": np.random.uniform(10, 120, len(zones)),
    })
    
    # Dataset de ruido
    datasets["ruido"] = pd.DataFrame({
        "zona": zones,
        "ruido_db": np.random.uniform(55, 85, len(zones)),
    })
    
    # Dataset de zonas verdes
    datasets["verdes"] = pd.DataFrame({
        "zona": zones,
        "hectareas_verdes": np.random.uniform(2, 30, len(zones)),
        "habitantes_por_ha": np.random.uniform(500, 5000, len(zones)),
    })
    
    # Dataset de actividad comercial
    datasets["comercio"] = pd.DataFrame({
        "zona": zones,
        "num_comercios": np.random.randint(20, 200, len(zones)),
        "empleo": np.random.randint(100, 1000, len(zones)),
    })
    
    # Dataset de servicios públicos
    datasets["servicios"] = pd.DataFrame({
        "zona": zones,
        "centros_salud": np.random.randint(0, 3, len(zones)),
        "escuelas": np.random.randint(0, 5, len(zones)),
        "bibliotecas": np.random.randint(0, 2, len(zones)),
    })
    
    # Dataset de quejas/incidencias (simulado)
    datasets["quejas"] = pd.DataFrame({
        "zona": zones,
        "num_quejas": np.random.randint(50, 400, len(zones)),
    })
    
    return datasets
