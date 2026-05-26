"""
Data Cleaning Module
Limpieza y preparación de datos
"""

import pandas as pd
import numpy as np
from typing import Tuple


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas
    
    Args:
        df: DataFrame a normalizar
        
    Returns:
        pd.DataFrame: DataFrame con columnas normalizadas
    """
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    df.columns = df.columns.str.replace("[áàäâ]", "a", regex=True)
    df.columns = df.columns.str.replace("[éèëê]", "e", regex=True)
    df.columns = df.columns.str.replace("[íìïî]", "i", regex=True)
    df.columns = df.columns.str.replace("[óòöô]", "o", regex=True)
    df.columns = df.columns.str.replace("[úùüû]", "u", regex=True)
    return df


def clean_numeric_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia valores numéricos: NaN, infinitos, outliers
    
    Args:
        df: DataFrame a limpiar
        
    Returns:
        pd.DataFrame: DataFrame limpio
    """
    df = df.copy()
    
    # Selecciona solo columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        # Reemplaza infinitos por NaN
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        
        # Rellena NaN con la mediana
        if df[col].isna().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    return df


def remove_duplicates(df: pd.DataFrame, subset: str = None) -> pd.DataFrame:
    """
    Elimina duplicados
    
    Args:
        df: DataFrame a limpiar
        subset: Columna para detectar duplicados. Si None, usa todas
        
    Returns:
        pd.DataFrame: DataFrame sin duplicados
    """
    df = df.copy()
    if subset:
        df = df.drop_duplicates(subset=[subset])
    else:
        df = df.drop_duplicates()
    return df.reset_index(drop=True)


def handle_missing_values(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
    """
    Maneja valores faltantes
    
    Args:
        df: DataFrame a limpiar
        strategy: 'mean', 'median', 'forward_fill', 'drop'
        
    Returns:
        pd.DataFrame: DataFrame con valores faltantes tratados
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if strategy == "median":
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
    elif strategy == "mean":
        for col in numeric_cols:
            df[col].fillna(df[col].mean(), inplace=True)
    elif strategy == "forward_fill":
        df[numeric_cols] = df[numeric_cols].fillna(method='ffill').fillna(method='bfill')
    elif strategy == "drop":
        df = df.dropna(subset=numeric_cols)
    
    return df


def normalize_minmax(data: np.ndarray) -> np.ndarray:
    """
    Normaliza datos usando Min-Max a rango [0, 1]
    
    Args:
        data: Array de datos
        
    Returns:
        np.ndarray: Datos normalizados
    """
    min_val = np.nanmin(data)
    max_val = np.nanmax(data)
    
    if min_val == max_val:
        return np.ones_like(data, dtype=float)
    
    return (data - min_val) / (max_val - min_val)


def normalize_zscore(data: np.ndarray) -> np.ndarray:
    """
    Normaliza datos usando Z-score
    
    Args:
        data: Array de datos
        
    Returns:
        np.ndarray: Datos normalizados
    """
    mean = np.nanmean(data)
    std = np.nanstd(data)
    
    if std == 0:
        return np.zeros_like(data, dtype=float)
    
    return (data - mean) / std


def aggregate_by_zone(df: pd.DataFrame, zone_col: str, agg_methods: dict = None) -> pd.DataFrame:
    """
    Agrega datos por zona
    
    Args:
        df: DataFrame a agregar
        zone_col: Nombre de columna de zona
        agg_methods: Dict con métodos de agregación por columna
        
    Returns:
        pd.DataFrame: Datos agregados por zona
    """
    if agg_methods is None:
        # Por defecto: media para números, contar para el resto
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        agg_methods = {col: "mean" for col in numeric_cols}
    
    df_agg = df.groupby(zone_col, as_index=False).agg(agg_methods)
    return df_agg


def create_feature_bins(df: pd.DataFrame, column: str, bins: int = 5) -> pd.Series:
    """
    Crea bins categóricos a partir de datos numéricos
    
    Args:
        df: DataFrame
        column: Nombre de columna
        bins: Número de bins
        
    Returns:
        pd.Series: Serie con bins
    """
    return pd.cut(df[column], bins=bins, labels=False)


def detect_and_handle_outliers(df: pd.DataFrame, method: str = "iqr") -> pd.DataFrame:
    """
    Detecta y maneja outliers
    
    Args:
        df: DataFrame
        method: 'iqr' o 'zscore'
        
    Returns:
        pd.DataFrame: DataFrame con outliers tratados
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if method == "iqr":
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Reemplaza outliers con límites
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
    
    elif method == "zscore":
        for col in numeric_cols:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            df[col] = df[col].mask(z_scores > 3, df[col].mean())
    
    return df


def merge_datasets(dfs: dict, on: str = "zona", how: str = "outer") -> pd.DataFrame:
    """
    Fusiona múltiples datasets por columna común
    
    Args:
        dfs: Dict de DataFrames {nombre: df}
        on: Columna para merge
        how: 'outer', 'inner', 'left', 'right'
        
    Returns:
        pd.DataFrame: Datos fusionados
    """
    if not dfs:
        return pd.DataFrame()
    
    dfs_list = list(dfs.values())
    result = dfs_list[0].copy()
    
    for df in dfs_list[1:]:
        result = result.merge(df, on=on, how=how, suffixes=('', '_dup'))
    
    return result


def create_data_quality_report(df: pd.DataFrame) -> dict:
    """
    Crea reporte de calidad de datos
    
    Args:
        df: DataFrame a analizar
        
    Returns:
        dict: Reporte con estadísticas
    """
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "percent_missing": (df.isnull().sum() / len(df) * 100).to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "numeric_cols": df.select_dtypes(include=[np.number]).columns.tolist(),
        "categorical_cols": df.select_dtypes(include=['object']).columns.tolist(),
    }
    return report
