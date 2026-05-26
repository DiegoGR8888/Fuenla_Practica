"""
Maps Module
Visualización de datos geográficos
"""

import pandas as pd
import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
import pydeck as pdk
from typing import Optional
import numpy as np
from src.indicators import get_priority_color


def create_folium_map(
    df: pd.DataFrame,
    lat_col: str = "latitud",
    lon_col: str = "longitud",
    zone_col: str = "zona",
    color_col: str = "prioridad",
    popup_cols: list = None,
    zoom_start: int = 12,
) -> folium.Map:
    """
    Crea mapa interactivo con Folium
    
    Args:
        df: DataFrame con datos geográficos
        lat_col: Nombre de columna de latitud
        lon_col: Nombre de columna de longitud
        zone_col: Nombre de columna de zona
        color_col: Columna para colorear puntos
        popup_cols: Columnas a mostrar en popup
        zoom_start: Nivel de zoom inicial
        
    Returns:
        folium.Map: Mapa creado
    """
    
    # Coordenadas centrales de Fuenlabrada
    center_lat = 40.32 if lat_col not in df.columns else df[lat_col].mean()
    center_lon = -3.80 if lon_col not in df.columns else df[lon_col].mean()
    
    # Crea mapa base
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles="OpenStreetMap"
    )
    
    # Validar que existen las columnas necesarias
    if lat_col not in df.columns or lon_col not in df.columns:
        return m
    
    if popup_cols is None:
        popup_cols = ["zona", "indice_prioridad", "prioridad"]
    
    # Añade puntos al mapa
    for idx, row in df.iterrows():
        lat = row[lat_col]
        lon = row[lon_col]
        
        # Valida coordenadas
        if pd.isna(lat) or pd.isna(lon):
            continue
        
        # Determina color
        if color_col in row.index:
            color = get_priority_color(str(row[color_col]))
        else:
            color = "#007bff"
        
        # Crea popup
        popup_text = "<b>{}</b><br>".format(row.get(zone_col, "Desconocida"))
        for col in popup_cols:
            if col in row.index and col != zone_col:
                value = row[col]
                if isinstance(value, (int, float)):
                    popup_text += "{}: {:.1f}<br>".format(col, value)
                else:
                    popup_text += "{}: {}<br>".format(col, value)
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            popup=folium.Popup(popup_text, max_width=300),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7,
            weight=2,
        ).add_to(m)
    
    # Añade control de capas
    folium.LayerControl().add_to(m)
    
    return m


def create_heatmap(
    df: pd.DataFrame,
    lat_col: str = "latitud",
    lon_col: str = "longitud",
    value_col: str = "indice_prioridad",
    zoom_start: int = 12,
) -> folium.Map:
    """
    Crea mapa de calor
    
    Args:
        df: DataFrame con datos
        lat_col: Columna de latitud
        lon_col: Columna de longitud
        value_col: Columna con valores para el calor
        zoom_start: Nivel de zoom
        
    Returns:
        folium.Map: Mapa de calor
    """
    
    center_lat = 40.32 if lat_col not in df.columns else df[lat_col].mean()
    center_lon = -3.80 if lon_col not in df.columns else df[lon_col].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles="OpenStreetMap"
    )
    
    # Prepara datos para heatmap
    if lat_col in df.columns and lon_col in df.columns and value_col in df.columns:
        heat_data = []
        for idx, row in df.iterrows():
            if not pd.isna(row[lat_col]) and not pd.isna(row[lon_col]) and not pd.isna(row[value_col]):
                # Normaliza valor para el calor [0, 1]
                normalized_value = row[value_col] / 100 if row[value_col] > 0 else 0
                heat_data.append([row[lat_col], row[lon_col], normalized_value])
        
        if heat_data:
            plugins.HeatMap(heat_data, radius=20, blur=15, max_zoom=1).add_to(m)
    
    return m


def create_pydeck_map(
    df: pd.DataFrame,
    lat_col: str = "latitud",
    lon_col: str = "longitud",
    color_col: str = "indice_prioridad",
) -> pdk.Deck:
    """
    Crea visualización con PyDeck
    
    Args:
        df: DataFrame con datos
        lat_col: Columna de latitud
        lon_col: Columna de longitud
        color_col: Columna para colorear
        
    Returns:
        pdk.Deck: Visualización PyDeck
    """
    
    if lat_col not in df.columns or lon_col not in df.columns:
        return None
    
    # Prepara datos
    plot_data = df[[lat_col, lon_col, color_col]].copy()
    plot_data.columns = ["latitude", "longitude", "color_value"]
    
    # Normaliza colores
    min_val = plot_data["color_value"].min()
    max_val = plot_data["color_value"].max()
    if max_val > min_val:
        plot_data["color_value"] = (plot_data["color_value"] - min_val) / (max_val - min_val) * 255
    
    # Crea layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        plot_data,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=20,
        radius_min_pixels=5,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position="[longitude, latitude]",
        get_fill_color="[color_value, 255 - color_value, 100]",
        get_line_color=[0, 0, 0],
    )
    
    # Coordenada central
    view_state = pdk.ViewState(
        longitude=df[lon_col].mean(),
        latitude=df[lat_col].mean(),
        zoom=12,
        pitch=45,
    )
    
    # Crea deck
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{zona}: {color_value:.1f}"}
    )
    
    return deck


def plot_priority_distribution_map(
    df: pd.DataFrame,
    lat_col: str = "latitud",
    lon_col: str = "longitud",
) -> folium.Map:
    """
    Crea mapa con color por nivel de prioridad
    
    Args:
        df: DataFrame
        lat_col: Columna de latitud
        lon_col: Columna de longitud
        
    Returns:
        folium.Map: Mapa coloreado
    """
    
    center_lat = 40.32 if lat_col not in df.columns else df[lat_col].mean()
    center_lon = -3.80 if lon_col not in df.columns else df[lon_col].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )
    
    if lat_col in df.columns and lon_col in df.columns:
        # Capa para cada nivel de prioridad
        for priority in ["Baja", "Media", "Alta", "Crítica"]:
            priority_data = df[df["prioridad"] == priority]
            
            if len(priority_data) > 0:
                feature_group = folium.FeatureGroup(
                    name=f"Prioridad {priority}",
                    show=True
                )
                
                for idx, row in priority_data.iterrows():
                    if not pd.isna(row[lat_col]) and not pd.isna(row[lon_col]):
                        color = get_priority_color(priority)
                        
                        popup_text = "<b>{}</b><br>".format(row.get("zona", "?"))
                        popup_text += "Índice: {:.1f}<br>".format(row.get("indice_prioridad", 0))
                        popup_text += "Prioridad: {}".format(priority)
                        
                        folium.CircleMarker(
                            location=[row[lat_col], row[lon_col]],
                            radius=12,
                            popup=folium.Popup(popup_text, max_width=300),
                            color=color,
                            fill=True,
                            fillColor=color,
                            fillOpacity=0.8,
                            weight=2,
                        ).add_to(feature_group)
                
                feature_group.add_to(m)
    
    folium.LayerControl().add_to(m)
    return m


def create_zone_comparison_map(
    df: pd.DataFrame,
    compare_col: str,
    lat_col: str = "latitud",
    lon_col: str = "longitud",
) -> folium.Map:
    """
    Crea mapa comparativo de un indicador
    
    Args:
        df: DataFrame
        compare_col: Columna a comparar
        lat_col: Columna de latitud
        lon_col: Columna de longitud
        
    Returns:
        folium.Map: Mapa comparativo
    """
    
    center_lat = 40.32 if lat_col not in df.columns else df[lat_col].mean()
    center_lon = -3.80 if lon_col not in df.columns else df[lon_col].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )
    
    if lat_col in df.columns and lon_col in df.columns and compare_col in df.columns:
        # Normaliza valores para color
        min_val = df[compare_col].min()
        max_val = df[compare_col].max()
        
        for idx, row in df.iterrows():
            if pd.isna(row[lat_col]) or pd.isna(row[lon_col]) or pd.isna(row[compare_col]):
                continue
            
            # Color según valor normalizado (azul=bajo, rojo=alto)
            if max_val > min_val:
                normalized = (row[compare_col] - min_val) / (max_val - min_val)
            else:
                normalized = 0.5
            
            # Gradiente de color
            r = int(normalized * 255)
            g = int((1 - normalized) * 255)
            b = 100
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            popup_text = "<b>{}</b><br>".format(row.get("zona", "?"))
            popup_text += "{}: {:.2f}".format(compare_col, row[compare_col])
            
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=10,
                popup=folium.Popup(popup_text, max_width=300),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2,
            ).add_to(m)
    
    return m
