"""
Urban Priority Indicator Module
Calcula el Índice de Prioridad Urbana
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from src.cleaning import normalize_minmax


def normalize_column_inverse(data: np.ndarray) -> np.ndarray:
    """
    Normaliza columnas inversas: menor valor = mayor prioridad.
    Convierte siempre a número para evitar errores con columnas de texto
    o dtypes Arrow de pandas.
    """
    data = pd.to_numeric(pd.Series(data), errors="coerce").fillna(0).to_numpy(dtype=float)

    min_val = np.nanmin(data)
    max_val = np.nanmax(data)

    if min_val == max_val:
        return np.ones_like(data, dtype=float)

    normalized = (data - min_val) / (max_val - min_val)
    return 1.0 - normalized


def numeric_series(df: pd.DataFrame, col: str) -> pd.Series:
    """Devuelve una columna convertida a numérica de forma segura."""
    return pd.to_numeric(df[col], errors="coerce").fillna(0)


def find_numeric_column(df: pd.DataFrame, keywords: list[str], default: str = None) -> str | None:
    """
    Busca una columna que contenga alguna palabra clave y que pueda convertirse a número.
    Evita coger columnas de texto como 'zona'.
    """
    candidate_cols = []

    if default and default in df.columns:
        candidate_cols.append(default)

    for c in df.columns:
        c_lower = c.lower()
        if any(k in c_lower for k in keywords):
            candidate_cols.append(c)

    for c in candidate_cols:
        converted = pd.to_numeric(df[c], errors="coerce")
        if converted.notna().sum() > 0:
            return c

    return None


def calculate_urban_priority_index(
    df: pd.DataFrame,
    weights: Dict[str, float] = None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Calcula el Índice de Prioridad Urbana
    
    Args:
        df: DataFrame con indicadores por zona
        weights: Dict con pesos de cada componente
                 Por defecto usa pesos predefinidos
        
    Returns:
        Tuple: (DataFrame con índice, Dict con detalles)
    """
    
    # Pesos por defecto según propuesta
    if weights is None:
        weights = {
            "quejas": 0.30,
            "contaminacion": 0.20,
            "ruido": 0.15,
            "zonas_verdes": 0.15,
            "servicios": 0.10,
            "comercio": 0.10,
        }
    
    df = df.copy()
    components = {}
    
    # 1. Componente de quejas (30%)
    if "quejas" in df.columns or "num_quejas" in df.columns:
        col = "quejas" if "quejas" in df.columns else "num_quejas"
        df["quejas_norm"] = normalize_minmax(numeric_series(df, col).values) * 100
        components["quejas"] = weights["quejas"]
    else:
        df["quejas_norm"] = 0
        components["quejas"] = 0
    
    # 2. Componente de contaminación (20%)
    if "contaminacion" in df.columns or "pm10" in df.columns or "PM10" in df.columns:
        # Busca columnas de contaminación
        contam_cols = [col for col in df.columns if 
                      any(x in col.lower() for x in ["pm10", "pm25", "no2", "contam"])]
        
        if contam_cols:
            # Usa el promedio de columnas de contaminación
            contam_data = df[contam_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1, skipna=True).fillna(0)
        else:
            contam_data = df.get("contaminacion", pd.Series(0, index=df.index))
        
        df["contaminacion_norm"] = normalize_minmax(contam_data.values) * 100
        components["contaminacion"] = weights["contaminacion"]
    else:
        df["contaminacion_norm"] = 0
        components["contaminacion"] = 0
    
    # 3. Componente de ruido (15%)
    if "ruido" in df.columns or "ruido_db" in df.columns or "ruido_decibelios" in df.columns:
        col = "ruido"
        for c in df.columns:
            if any(x in c.lower() for x in ["ruido", "db", "decibelio"]):
                col = c
                break
        df["ruido_norm"] = normalize_minmax(numeric_series(df, col).values) * 100
        components["ruido"] = weights["ruido"]
    else:
        df["ruido_norm"] = 0
        components["ruido"] = 0
    
    # 4. Componente de zonas verdes (15%)
    # INVERTIDO: menos zonas verdes = más prioridad
    if "zonas_verdes" in df.columns or "hectareas_verdes" in df.columns or "zonas_verdes_ha" in df.columns:
        # IMPORTANTE: no buscar por "zona", porque cogería la columna de texto "zona".
        col = find_numeric_column(
            df,
            keywords=["zonas_verdes", "verde", "hectarea", "ha", "superficie"],
            default="zonas_verdes"
        )
        if col is None:
            df["zonas_verdes_norm"] = 0
            components["zonas_verdes"] = 0
        else:
            df["zonas_verdes_norm"] = normalize_column_inverse(df[col].values) * 100
            components["zonas_verdes"] = weights["zonas_verdes"]
    else:
        df["zonas_verdes_norm"] = 0
        components["zonas_verdes"] = 0

    # 5. Componente de servicios públicos (10%)
    # INVERTIDO: menos servicios = más prioridad
    if "servicios_publicos" in df.columns or "servicios" in df.columns:
        col = find_numeric_column(
            df,
            keywords=["servicio", "salud", "escuela", "biblioteca"],
            default="servicios_publicos" if "servicios_publicos" in df.columns else "servicios"
        )
        if col is None:
            df["servicios_norm"] = 0
            components["servicios"] = 0
        else:
            df["servicios_norm"] = normalize_column_inverse(df[col].values) * 100
            components["servicios"] = weights["servicios"]
    else:
        df["servicios_norm"] = 0
        components["servicios"] = 0

    # 6. Componente de actividad comercial (10%)
    # INVERTIDO: menos actividad comercial = más prioridad
    if "actividad_comercial" in df.columns or "num_comercios" in df.columns or "comercio" in df.columns:
        col = find_numeric_column(
            df,
            keywords=["actividad_comercial", "comercial", "comercio", "num_comercios", "empleo"],
            default="actividad_comercial"
        )
        if col is None:
            df["comercio_norm"] = 0
            components["comercio"] = 0
        else:
            df["comercio_norm"] = normalize_column_inverse(df[col].values) * 100
            components["comercio"] = weights["comercio"]
    else:
        df["comercio_norm"] = 0
        components["comercio"] = 0

    # Calcula índice ponderado
    total_weight = sum(components.values())
    if total_weight > 0:
        df["indice_prioridad"] = (
            (df["quejas_norm"] * components["quejas"] +
             df["contaminacion_norm"] * components["contaminacion"] +
             df["ruido_norm"] * components["ruido"] +
             df["zonas_verdes_norm"] * components["zonas_verdes"] +
             df["servicios_norm"] * components["servicios"] +
             df["comercio_norm"] * components["comercio"])
            / total_weight
        )
    else:
        df["indice_prioridad"] = 0
    
    # Clasifica prioridad
    df["prioridad"] = pd.cut(
        df["indice_prioridad"],
        bins=[0, 40, 60, 80, 100],
        labels=["Baja", "Media", "Alta", "Crítica"],
        include_lowest=True
    )
    
    # Información de componentes
    details = {
        "components": components,
        "total_weight": total_weight,
        "normalizations": {
            "quejas": "Min-Max",
            "contaminacion": "Min-Max",
            "ruido": "Min-Max",
            "zonas_verdes": "Min-Max Invertido",
            "servicios": "Min-Max Invertido",
            "comercio": "Min-Max Invertido",
        }
    }
    
    return df, details


def calculate_priority_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la contribución de cada componente al índice
    
    Args:
        df: DataFrame con columnas normalizadas
        
    Returns:
        pd.DataFrame: Desglose de contribuciones
    """
    breakdown = df[["zona", "indice_prioridad"]].copy()
    
    # Calcula contribuciones con pesos
    weights = {
        "quejas": 0.30,
        "contaminacion": 0.20,
        "ruido": 0.15,
        "zonas_verdes": 0.15,
        "servicios": 0.10,
        "comercio": 0.10,
    }
    
    for component, weight in weights.items():
        col = f"{component}_norm"
        if col in df.columns:
            breakdown[f"{component}_contrib"] = df[col] * weight
    
    return breakdown


def classify_priority(index: float) -> str:
    """
    Clasifica un índice de prioridad
    
    Args:
        index: Valor del índice (0-100)
        
    Returns:
        str: Clasificación
    """
    if index < 40:
        return "Baja"
    elif index < 60:
        return "Media"
    elif index < 80:
        return "Alta"
    else:
        return "Crítica"


def get_priority_color(priority: str) -> str:
    """
    Retorna color para cada nivel de prioridad
    
    Args:
        priority: Nivel de prioridad
        
    Returns:
        str: Código de color hex
    """
    colors = {
        "Baja": "#28a745",      # Verde
        "Media": "#ffc107",     # Amarillo
        "Alta": "#fd7e14",      # Naranja
        "Crítica": "#dc3545",   # Rojo
    }
    return colors.get(priority, "#6c757d")


def get_priority_emoji(priority: str) -> str:
    """
    Retorna emoji para cada nivel de prioridad
    
    Args:
        priority: Nivel de prioridad
        
    Returns:
        str: Emoji
    """
    emojis = {
        "Baja": "✅",
        "Media": "⚠️",
        "Alta": "🔴",
        "Crítica": "🚨",
    }
    return emojis.get(priority, "❓")


def calculate_social_impact_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula puntuación de impacto social
    
    Args:
        df: DataFrame
        
    Returns:
        pd.DataFrame: Con columna de impacto social
    """
    df = df.copy()
    
    # Social: quejas + falta de servicios
    social_score = 0
    if "quejas_norm" in df.columns:
        social_score += df["quejas_norm"] * 0.6
    if "servicios_norm" in df.columns:
        social_score += df["servicios_norm"] * 0.4
    
    df["impacto_social"] = social_score
    return df


def calculate_environmental_impact_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula puntuación de impacto ambiental
    
    Args:
        df: DataFrame
        
    Returns:
        pd.DataFrame: Con columna de impacto ambiental
    """
    df = df.copy()
    
    # Ambiental: contaminación + ruido + zonas verdes
    env_score = 0
    if "contaminacion_norm" in df.columns:
        env_score += df["contaminacion_norm"] * 0.4
    if "ruido_norm" in df.columns:
        env_score += df["ruido_norm"] * 0.3
    if "zonas_verdes_norm" in df.columns:
        env_score += df["zonas_verdes_norm"] * 0.3
    
    df["impacto_ambiental"] = env_score
    return df


def calculate_economic_impact_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula puntuación de impacto económico
    
    Args:
        df: DataFrame
        
    Returns:
        pd.DataFrame: Con columna de impacto económico
    """
    df = df.copy()
    
    # Económico: actividad comercial + servicios
    econ_score = 0
    if "comercio_norm" in df.columns:
        econ_score += df["comercio_norm"] * 0.7
    if "servicios_norm" in df.columns:
        econ_score += df["servicios_norm"] * 0.3
    
    df["impacto_economico"] = econ_score
    return df
