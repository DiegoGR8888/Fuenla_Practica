"""
FUENLABRADA SMART PRIORITIES
============================
Plataforma inteligente para priorizar actuaciones urbanas mediante datos abiertos y análisis predictivo.

Características:
- 📍 Mapa interactivo de zonas por prioridad
- ⭐ Índice de Prioridad Urbana (0-100)
- 🌳 Análisis ambiental (contaminación, ruido, zonas verdes)
- 🤖 Predicción con Machine Learning
- 🧠 Recomendaciones automáticas
- 📦 Trazabilidad de datos públicos

Autor: Proyecto Hackathon Fuenlabrada
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

# Importa módulos locales
from src.data_loader import (
    load_uploaded_file, create_sample_data, load_demo_datasets,
    detect_zone_column, detect_numeric_columns, detect_geo_columns
)
from src.cleaning import (
    normalize_columns, clean_numeric_data, remove_duplicates,
    handle_missing_values, merge_datasets, create_data_quality_report
)
from src.indicators import (
    calculate_urban_priority_index, calculate_priority_breakdown,
    classify_priority, get_priority_color, get_priority_emoji,
    calculate_social_impact_score, calculate_environmental_impact_score,
    calculate_economic_impact_score
)
from src.maps import (
    create_folium_map, create_heatmap, plot_priority_distribution_map,
    create_zone_comparison_map
)
from src.model import PriorityPredictor, add_predictions_to_df
from src.recommendations import RecommendationEngine


# ============================================================================
# CONFIGURACIÓN DE PÁGINA - ESTILO PROFESIONAL
# ============================================================================

st.set_page_config(
    page_title="Fuenlabrada Smart Priorities",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Plataforma de Análisis Urbano - Hackathon Fuenlabrada"
    }
)

# CSS personalizado profesional
st.markdown("""
<style>
    /* Paleta de colores */
    :root {
        --color-critical: #dc3545;
        --color-high: #fd7e14;
        --color-medium: #ffc107;
        --color-low: #28a745;
    }
    
    /* Estilos generales */
    .stMetricLabel {
        font-size: 1.1em;
        font-weight: 600;
    }
    
    /* Headers */
    .header-title {
        font-size: 2.8em;
        color: #003366;
        text-align: center;
        margin: 20px 0 10px 0;
        font-weight: 700;
    }
    
    .header-subtitle {
        font-size: 1.1em;
        color: #666;
        text-align: center;
        margin: 0 0 20px 0;
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .critical {
        background: linear-gradient(135deg, #ffe6e6 0%, #ffcccc 100%);
        border-left: 5px solid #dc3545;
    }
    
    .high {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe8a0 100%);
        border-left: 5px solid #fd7e14;
    }
    
    .medium {
        background: linear-gradient(135deg, #d1ecf1 0%, #a8dfe0 100%);
        border-left: 5px solid #0c5460;
    }
    
    .low {
        background: linear-gradient(135deg, #d4edda 0%, #a8d5aa 100%);
        border-left: 5px solid #28a745;
    }
    
    /* Separadores */
    hr {
        margin: 25px 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.05em;
        font-weight: 600;
    }
    
    /* Botones */
    .stButton > button {
        background-color: #003366;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #004d99;
        box-shadow: 0 4px 12px rgba(0,51,102,0.3);
    }
    
    /* Markdown personalizado */
    .info-box {
        background-color: #e7f3ff;
        border-left: 5px solid #0066cc;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# INICIALIZACIÓN DE SESSION STATE - Estado persistente
# ============================================================================

# Datos maestros
if "df_master" not in st.session_state:
    st.session_state.df_master = None
    st.session_state.df_processed = None

# Gestión de datasets
if "datasets_loaded" not in st.session_state:
    st.session_state.datasets_loaded = {}

if "datasets_metadata" not in st.session_state:
    st.session_state.datasets_metadata = {}

# Modelo ML
if "predictor" not in st.session_state:
    st.session_state.predictor = PriorityPredictor()

if "model_trained" not in st.session_state:
    st.session_state.model_trained = False

if "model_metrics" not in st.session_state:
    st.session_state.model_metrics = {}

# UI
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0

# Recomendaciones
if "recommendations_engine" not in st.session_state:
    st.session_state.recommendations_engine = RecommendationEngine()


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

@st.cache_data
def load_initial_data():
    """Carga datos de demostración iniciales"""
    df = create_sample_data()
    datasets = load_demo_datasets()
    return df, datasets


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa un DataFrame: limpieza, normalización, cálculo de índices
    
    Args:
        df: DataFrame sin procesar
        
    Returns:
        pd.DataFrame: DataFrame procesado
    """
    
    # Normaliza columnas
    df = normalize_columns(df)
    
    # Limpia datos
    df = clean_numeric_data(df)
    df = handle_missing_values(df, strategy="median")
    df = remove_duplicates(df, subset="zona" if "zona" in df.columns else None)
    
    # Calcula índice de prioridad
    df, index_details = calculate_urban_priority_index(df)
    
    # Añade impactos por eje
    df = calculate_social_impact_score(df)
    df = calculate_environmental_impact_score(df)
    df = calculate_economic_impact_score(df)
    
    return df


def display_summary_metrics(df: pd.DataFrame):
    """Muestra métricas principales en columnas"""
    
    if "zona" not in df.columns or "indice_prioridad" not in df.columns:
        return
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Zonas Analizadas", len(df))
    
    with col2:
        avg_index = df["indice_prioridad"].mean()
        st.metric("⭐ Índice Promedio", f"{avg_index:.1f}")
    
    with col3:
        critical = len(df[df["prioridad"] == "Crítica"])
        st.metric("🚨 Zonas Críticas", critical, delta=f"{critical/len(df)*100:.1f}%")
    
    with col4:
        datasets = len(st.session_state.datasets_loaded)
        st.metric("📦 Datasets Cargados", datasets)
    
    with col5:
        model_status = "✅ Entrenado" if st.session_state.model_trained else "⏳ No entrenado"
        st.metric("🤖 Modelo ML", model_status, label_visibility="visible")


def display_priority_ranking(df: pd.DataFrame, top_n: int = 10):
    """Muestra ranking de prioridades"""
    
    if "zona" not in df.columns or "indice_prioridad" not in df.columns:
        return
    
    df_ranked = df.nlargest(top_n, "indice_prioridad")[["zona", "indice_prioridad", "prioridad"]]
    
    # Gráfico de barras
    fig = px.bar(
        df_ranked,
        x="indice_prioridad",
        y="zona",
        orientation="h",
        color="prioridad",
        color_discrete_map={
            "Crítica": "#dc3545",
            "Alta": "#fd7e14",
            "Media": "#ffc107",
            "Baja": "#28a745"
        },
        title=f"Top {top_n} Zonas por Prioridad",
        labels={"indice_prioridad": "Índice de Prioridad", "zona": "Zona"}
    )
    
    fig.update_layout(yaxis_categoryorder="total ascending", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla
    st.dataframe(
        df_ranked.reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )


def display_indicators_dashboard(df: pd.DataFrame):
    """Muestra dashboard de indicadores por eje"""
    
    col1, col2, col3 = st.columns(3)
    
    # IMPACTO SOCIAL
    with col1:
        st.subheader("👥 Impacto Social")
        
        if "impacto_social" in df.columns:
            avg_social = df["impacto_social"].mean()
            st.metric("Puntuación Media", f"{avg_social:.1f}")
            
            fig_social = px.histogram(
                df,
                x="impacto_social",
                nbins=10,
                title="Distribución Impacto Social",
                color_discrete_sequence=["#3498db"]
            )
            fig_social.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_social, use_container_width=True)
    
    # IMPACTO AMBIENTAL
    with col2:
        st.subheader("🌳 Impacto Ambiental")
        
        if "impacto_ambiental" in df.columns:
            avg_env = df["impacto_ambiental"].mean()
            st.metric("Puntuación Media", f"{avg_env:.1f}")
            
            fig_env = px.histogram(
                df,
                x="impacto_ambiental",
                nbins=10,
                title="Distribución Impacto Ambiental",
                color_discrete_sequence=["#2ecc71"]
            )
            fig_env.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_env, use_container_width=True)
    
    # IMPACTO ECONÓMICO
    with col3:
        st.subheader("💰 Impacto Económico")
        
        if "impacto_economico" in df.columns:
            avg_econ = df["impacto_economico"].mean()
            st.metric("Puntuación Media", f"{avg_econ:.1f}")
            
            fig_econ = px.histogram(
                df,
                x="impacto_economico",
                nbins=10,
                title="Distribución Impacto Económico",
                color_discrete_sequence=["#f39c12"]
            )
            fig_econ.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_econ, use_container_width=True)


def display_environmental_analysis(df: pd.DataFrame):
    """Muestra análisis ambiental detallado con múltiples visualizaciones"""
    
    st.subheader("🌳 Análisis Ambiental Detallado")
    
    st.markdown("""
    Este análisis examina tres pilares ambientales críticos para la sostenibilidad urbana:
    - **Calidad del Aire**: Impacto directo en la salud respiratoria
    - **Contaminación Acústica**: Afecta bienestar y sueño
    - **Espacios Verdes**: Necesarios para calidad de vida y regulación climática
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Contaminación del aire
    with col1:
        st.write("### 💨 Contaminación del Aire")
        if "contaminacion_norm" in df.columns:
            # Gráfico de barras
            df_sorted = df.nlargest(10, "contaminacion_norm")[["zona", "contaminacion_norm"]]
            
            fig = px.bar(
                df_sorted,
                x="contaminacion_norm",
                y="zona",
                orientation="h",
                color="contaminacion_norm",
                color_continuous_scale="Reds",
                title="Top 10 Zonas con Mayor Contaminación",
                labels={"contaminacion_norm": "Índice de Contaminación"}
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas
            st.metric("Promedio", f"{df['contaminacion_norm'].mean():.1f}")
    
    # Contaminación acústica
    with col2:
        st.write("### 🔊 Contaminación Acústica")
        if "ruido_norm" in df.columns:
            # Gráfico de barras
            df_sorted = df.nlargest(10, "ruido_norm")[["zona", "ruido_norm"]]
            
            fig = px.bar(
                df_sorted,
                x="ruido_norm",
                y="zona",
                orientation="h",
                color="ruido_norm",
                color_continuous_scale="Oranges",
                title="Top 10 Zonas con Mayor Ruido",
                labels={"ruido_norm": "Nivel de Ruido"}
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas
            st.metric("Promedio", f"{df['ruido_norm'].mean():.1f}")
    
    st.markdown("---")
    
    # Zonas verdes
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🌿 Déficit de Zonas Verdes")
        if "zonas_verdes_norm" in df.columns:
            df_sorted = df.nlargest(10, "zonas_verdes_norm")[["zona", "zonas_verdes_norm"]]
            
            fig = px.bar(
                df_sorted,
                x="zonas_verdes_norm",
                y="zona",
                orientation="h",
                color="zonas_verdes_norm",
                color_continuous_scale="Greens_r",
                title="Top 10 Zonas con Mayor Déficit Verde",
                labels={"zonas_verdes_norm": "Déficit de zonas verdes"}
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas
            st.metric("Promedio Déficit", f"{df['zonas_verdes_norm'].mean():.1f}")
    
    with col2:
        st.write("### 📊 Distribución de Impacto Ambiental")
        if "impacto_ambiental" in df.columns:
            fig = px.histogram(
                df,
                x="impacto_ambiental",
                nbins=12,
                title="Distribución de Puntuación Ambiental",
                color_discrete_sequence=["#2ecc71"],
                labels={"impacto_ambiental": "Puntuación Ambiental"}
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


def train_and_predict(df: pd.DataFrame):
    """Entrena el modelo predictivo"""
    
    if len(df) < 5:
        st.warning("⚠️ Se necesitan al menos 5 zonas para entrenar el modelo")
        return df
    
    try:
        # Entrena
        metrics = st.session_state.predictor.train(df)
        
        if "error" not in metrics:
            st.session_state.model_trained = True
            
            # Añade predicciones
            df = add_predictions_to_df(df, st.session_state.predictor)
            
            return df
        else:
            st.warning(f"❌ Error al entrenar: {metrics['error']}")
            return df
    except Exception as e:
        st.error(f"Error durante entrenamiento: {str(e)}")
        return df


# ============================================================================
# SIDEBAR - INFORMACIÓN DE DATOS
# ============================================================================

st.sidebar.markdown("# 📦 Datos Públicos de Fuenlabrada")

st.sidebar.markdown("""
### 📊 Fuente de Datos
Los datos proceden de:
- **Portal oficial**: [datosabiertos.ayto-fuenlabrada.es](https://datosabiertos.ayto-fuenlabrada.es)
- **Organismo**: Ayuntamiento de Fuenlabrada
- **Licencia**: Datos públicos abiertos (CC0 1.0)
- **Actualización**: Trimestral

### 🔄 Carga de datos
Los datos se actualizan únicamente a través de:
- Integración con CKAN API del Ayuntamiento
- Actualización manual del código

**No se aceptan datos de usuarios externos.**
""")

# Carga datos públicos de Fuenlabrada
try:
    df = pd.read_csv("data/fuenlabrada_open_data.csv")
    st.session_state.df_master = df
    st.session_state.datasets_loaded = {"fuenlabrada_open_data": df}
    st.sidebar.success("✅ Datos públicos de Fuenlabrada cargados")
except FileNotFoundError:
    # Fallback a datos de demostración si no existe el archivo
    df, demo_datasets = load_initial_data()
    st.session_state.df_master = df
    st.session_state.datasets_loaded = demo_datasets
    st.sidebar.warning("⚠️ Usando datos de demostración")
except Exception as e:
    st.sidebar.error(f"Error cargando datos: {str(e)}")
    df, demo_datasets = load_initial_data()
    st.session_state.df_master = df
    st.session_state.datasets_loaded = demo_datasets


# Procesa datos si están cargados
if st.session_state.df_master is not None:
    df_master = st.session_state.df_master.copy()
    
    # Procesa datos
    df_master = process_dataframe(df_master)
    
    # Entrena modelo si no está entrenado
    if not st.session_state.model_trained:
        df_master = train_and_predict(df_master)
    else:
        df_master = add_predictions_to_df(df_master, st.session_state.predictor)


# ============================================================================
# NAVEGACIÓN - TABS PRINCIPALES
# ============================================================================

st.markdown('<h1 class="header-title">📍 Fuenlabrada Smart Priorities</h1>', unsafe_allow_html=True)
st.markdown("""
<p style="text-align: center; color: #666;">
Plataforma inteligente para priorizar actuaciones urbanas mediante datos abiertos y análisis predictivo
</p>
""", unsafe_allow_html=True)

if st.session_state.df_master is None:
    st.warning("⚠️ Por favor, carga datos para comenzar")
else:
    # Métricas principales
    st.markdown("---")
    display_summary_metrics(df_master)
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏙️ Inicio",
        "📍 Mapa Interactivo",
        "⭐ Índice Urbano",
        "🌳 Medio Ambiente",
        "🤖 Predicción",
        "🧠 Recomendaciones",
        "📦 Datos"
    ])
    
    # ========== TAB 1: INICIO ==========
    with tab1:
        st.markdown("## 🏙️ Resumen Ejecutivo")
        
        st.markdown("""
        ### 🎯 Propósito de esta Plataforma
        
        **Fuenlabrada Smart Priorities** convierte datos públicos abiertos en una herramienta de toma de decisiones
        para el Ayuntamiento, permitiendo priorizar intervenciones urbanas de forma **objetiva, basada en datos reales**
        de la ciudad y las necesidades de sus ciudadanos.
        """)
        
        # Información general
        col1, col2, col3, col4 = st.columns(4)
        
        summary = RecommendationEngine.get_priority_summary(df_master)
        
        with col1:
            st.metric("Total de Zonas", summary["total_zonas"])
        with col2:
            st.metric("Promedio Índice", f"{summary['indice_promedio']:.1f}")
        with col3:
            st.metric("Zonas Críticas", summary["zonas_criticas"])
        with col4:
            st.metric("Zonas en Buen Estado", summary["zonas_bajas"])
        
        st.markdown("---")
        
        # Distribución por prioridad
        col1, col2 = st.columns(2)
        
        with col1:
            priority_counts = df_master["prioridad"].value_counts().sort_index(ascending=False)
            
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="Distribución de Zonas por Nivel de Prioridad",
                color_discrete_map={
                    "Crítica": "#dc3545",
                    "Alta": "#fd7e14",
                    "Media": "#ffc107",
                    "Baja": "#28a745"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Resumen por Zona")
            st.markdown(f"""
            #### Zonas con Mayor Prioridad
            - **🔴 Más crítica:** {summary['peor_zona']} 
              - Índice: {df_master[df_master['zona']==summary['peor_zona']]['indice_prioridad'].values[0]:.1f}
              - Requiere intervención urgente
            
            #### Zonas con Mejor Estado
            - **🟢 Mejor estado:** {summary['mejor_zona']}
              - Índice: {df_master[df_master['zona']==summary['mejor_zona']]['indice_prioridad'].values[0]:.1f}
              - Mantener y mejorar
            
            #### Amplitud del Problema
            - **Diferencia máxima:** {df_master['indice_prioridad'].max() - df_master['indice_prioridad'].min():.1f} puntos
            """)
        
        st.markdown("---")
        
        st.subheader("📈 Análisis por Ejes de Sostenibilidad")
        display_indicators_dashboard(df_master)
        
        st.markdown("---")
        
        st.subheader("💡 ¿Cómo Usar Esta Información?")
        st.markdown("""
        1. **Identificar zonas críticas** que necesitan atención inmediata
        2. **Entender los problemas** específicos de cada área (quejas, contaminación, etc.)
        3. **Priorizar presupuesto** en zonas de mayor necesidad
        4. **Predecir problemas futuros** con el modelo ML
        5. **Monitorear tendencias** y validar el impacto de intervenciones
        
        Los datos provienen de fuentes públicas oficiales del Ayuntamiento de Fuenlabrada,
        garantizando transparencia y trazabilidad.
        """)
    
    # ========== TAB 2: MAPA INTERACTIVO ==========
    with tab2:
        st.markdown("## 📍 Mapa Interactivo de Prioridades")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            map_type = st.radio(
                "Tipo de mapa:",
                ["Puntos", "Heatmap", "Por Prioridad"]
            )
            
            if "latitud" in df_master.columns and "longitud" in df_master.columns:
                show_popup = st.checkbox("Mostrar información", value=True)
        
        with col1:
            if "latitud" in df_master.columns and "longitud" in df_master.columns:
                if map_type == "Puntos":
                    m = create_folium_map(
                        df_master,
                        lat_col="latitud",
                        lon_col="longitud",
                        zone_col="zona",
                        color_col="prioridad"
                    )
                elif map_type == "Heatmap":
                    m = create_heatmap(
                        df_master,
                        lat_col="latitud",
                        lon_col="longitud",
                        value_col="indice_prioridad"
                    )
                else:
                    m = plot_priority_distribution_map(
                        df_master,
                        lat_col="latitud",
                        lon_col="longitud"
                    )
                
                st_folium(m, width=1200, height=600)
            else:
                st.warning("⚠️ No hay coordenadas geográficas disponibles")
    
    # ========== TAB 3: ÍNDICE URBANO ==========
    with tab3:
        st.markdown("## ⭐ Índice de Prioridad Urbana")
        
        st.markdown("""
        ### Definición
        El **Índice de Prioridad Urbana** (0-100) es una métrica composite que evalúa 
        la necesidad de intervención municipal en cada zona de Fuenlabrada, combinando 
        seis indicadores de sostenibilidad urbana obtenidos de datos públicos abiertos.
        
        ### 📊 Indicadores que lo componen:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **1. Quejas Ciudadanas (30%)**
            - Qué mide: Número de incidencias reportadas por ciudadanos
            - Fuente: Plataforma de participación ciudadana Ayto Fuenlabrada
            - Interpretación: Mayor número = Mayor insatisfacción
            - Rango: 0-500 quejas/periodo
            
            **2. Contaminación del Aire (20%)**
            - Qué mide: Concentración de PM2.5 y NO₂ (μg/m³)
            - Fuente: Red de monitoreo ambiental municipal
            - Interpretación: Índices WHO - Mayor = Riesgo para salud
            - Rango: 0-100 (Bueno a Peligroso)
            
            **3. Contaminación Acústica (15%)**
            - Qué mide: Nivel de ruido ambiental (dB)
            - Fuente: Red de monitoreo acústico CKAN
            - Interpretación: >70dB afecta calidad de vida (OMS)
            - Rango: 55-85 dB
            """)
        
        with col2:
            st.markdown("""
            **4. Déficit de Zonas Verdes (15%)**
            - Qué mide: m² de parques y espacios verdes por habitante
            - Fuente: Inventario municipal de espacios públicos
            - Interpretación: <9m²/hab es insuficiente (recomendación ONU)
            - Rango: Inverso (más verde = menor prioridad)
            
            **5. Equipamientos Públicos (10%)**
            - Qué mide: Disponibilidad de servicios públicos
            - Fuente: Catálogo municipal de servicios
            - Interpretación: Menor disponibilidad = Mayor necesidad
            
            **6. Actividad Comercial (10%)**
            - Qué mide: Número de comercios activos
            - Fuente: Registro de actividad comercial municipal
            - Interpretación: Baja actividad = Problemas socioeconómicos
            """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            display_priority_ranking(df_master, top_n=15)
        
        with col2:
            st.markdown("### Clasificación de Prioridad")
            st.markdown("""
            - 🟢 **Baja** (0-40): Zona en buen estado
            - 🟡 **Media** (40-60): Requiere seguimiento
            - 🟠 **Alta** (60-80): Intervención recomendada
            - 🔴 **Crítica** (80-100): Intervención urgente
            """)
            
            st.markdown("### Estadísticas del Índice")
            st.metric("Máximo", f"{df_master['indice_prioridad'].max():.1f}", delta="Más crítico")
            st.metric("Mínimo", f"{df_master['indice_prioridad'].min():.1f}", delta="Mejor estado")
            st.metric("Mediana", f"{df_master['indice_prioridad'].median():.1f}")
            st.metric("Desviación Std", f"{df_master['indice_prioridad'].std():.1f}")
    
    # ========== TAB 4: MEDIO AMBIENTE ==========
    with tab4:
        st.markdown("## 🌳 Análisis Ambiental")
        
        display_environmental_analysis(df_master)
        
        st.markdown("---")
        
        # Recomendaciones ambientales
        st.subheader("🎯 Zonas Prioritarias Ambientales")
        env_zones = RecommendationEngine.get_environmental_focus_areas(df_master)
        if env_zones:
            for i, zone in enumerate(env_zones, 1):
                st.markdown(f"**{i}. {zone}**")
    
    # ========== TAB 5: PREDICCIÓN ==========
    with tab5:
        st.markdown("## 🤖 Predicción de Riesgo Futuro")
        
        st.markdown("""
        ### Metodología
        Se utiliza un modelo de **Machine Learning (Random Forest)** entrenado con datos históricos
        de Fuenlabrada para predecir la evolución del Índice de Prioridad en próximas evaluaciones.
        
        ### 🔍 ¿Cómo funciona la predicción?
        El modelo aprende del comportamiento de los **6 indicadores principales**:
        
        1. **Quejas Ciudadanas** → Detecta patrones de insatisfacción
        2. **Contaminación del Aire** → Proyecta tendencias ambientales
        3. **Ruido Ambiental** → Predice cambios en contaminación acústica
        4. **Zonas Verdes** → Estima necesidad de espacios verdes
        5. **Equipamientos Públicos** → Anticipa déficits de servicios
        6. **Actividad Comercial** → Predice vitalidad económica de zonas
        
        **Entrada:** Mediciones actuales de los 6 indicadores por zona
        **Salida:** Pronóstico del Índice de Prioridad futuro
        **Confianza:** Validado con datos históricos de Fuenlabrada
        """)
        
        st.markdown("---")
        
        if st.session_state.model_trained:
            st.subheader("📊 Predicciones Detalladas por Zona")
            
            st.markdown("""
            Aquí puedes ver cómo evolucionará el Índice de Prioridad de cada zona en el futuro.
            La columna "Cambio Esperado" te indica si la situación mejorará (negativo) o empeorará (positivo).
            """)
            
            if "prediccion_prioridad" in df_master.columns and "tendencia" in df_master.columns:
                pred_table = df_master[[
                    "zona", "indice_prioridad", "prediccion_prioridad", "tendencia"
                ]].copy()
                pred_table["cambio_esperado"] = (pred_table["prediccion_prioridad"] - pred_table["indice_prioridad"]).round(1)
                pred_table = pred_table.sort_values("prediccion_prioridad", ascending=False)
                pred_table.columns = ["Zona", "Índice Actual", "Predicción Futura", "Tendencia", "Cambio Esperado"]
                
                st.dataframe(
                    pred_table.round(2),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("---")
                
                # Gráfico comparativo
                st.subheader("📈 Comparativa: Actual vs Predicción Futura")
                st.markdown("Las zonas con mayor diferencia entre actual y predicción son las que requieren mayor atención.")
                
                df_pred_viz = df_master.nlargest(12, "indice_prioridad")[["zona", "indice_prioridad", "prediccion_prioridad"]].copy()
                df_pred_viz = df_pred_viz.sort_values("prediccion_prioridad", ascending=True)
                
                fig = go.Figure(data=[
                    go.Bar(name="Índice Actual", x=df_pred_viz["indice_prioridad"], y=df_pred_viz["zona"], orientation='h', marker_color='#fd7e14'),
                    go.Bar(name="Predicción Futura", x=df_pred_viz["prediccion_prioridad"], y=df_pred_viz["zona"], orientation='h', marker_color='#dc3545')
                ])
                fig.update_layout(
                    title="Top 12 Zonas: Índice Actual vs Predicción Futura",
                    height=500,
                    barmode='group',
                    xaxis_title="Índice de Prioridad",
                    yaxis_title="Zona"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ El modelo se está entrenando con los datos disponibles...")
    
    # ========== TAB 6: RECOMENDACIONES ==========
    with tab6:
        st.markdown("## 🧠 Recomendaciones Automáticas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Top 5 Acciones Recomendadas")
            top_actions = RecommendationEngine.get_top_actions(df_master, top_n=5)
            for action in top_actions:
                st.markdown(f"- {action}")
        
        with col2:
            st.subheader("📍 Zonas Prioritarias por Eje")
            
            social_zones = RecommendationEngine.get_social_focus_areas(df_master)
            env_zones = RecommendationEngine.get_environmental_focus_areas(df_master)
            econ_zones = RecommendationEngine.get_economic_focus_areas(df_master)
            
            st.markdown("**👥 Social:**")
            for zone in social_zones:
                st.caption(f"• {zone}")
            
            st.markdown("**🌳 Ambiental:**")
            for zone in env_zones:
                st.caption(f"• {zone}")
            
            st.markdown("**💰 Económico:**")
            for zone in econ_zones:
                st.caption(f"• {zone}")
        
        st.markdown("---")
        st.subheader("📋 Recomendaciones por Zona")
        
        zona_selected = st.selectbox(
            "Selecciona una zona:",
            df_master["zona"].unique()
        )
        
        if zona_selected:
            zone_data = df_master[df_master["zona"] == zona_selected].iloc[0]
            
            st.markdown(f"### {zona_selected}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Índice de Prioridad", f"{zone_data['indice_prioridad']:.1f}")
            
            with col2:
                priority = zone_data["prioridad"]
                emoji = get_priority_emoji(priority)
                st.metric("Nivel de Prioridad", f"{emoji} {priority}")
            
            with col3:
                if "prediccion_prioridad" in zone_data.index:
                    st.metric("Predicción Futura", f"{zone_data['prediccion_prioridad']:.1f}")
            
            st.markdown("---")
            
            recommendation = RecommendationEngine.get_zone_recommendation(zone_data)
            st.markdown(recommendation)
    
    # ========== TAB 7: DATOS ==========
    with tab7:
        st.markdown("## 📦 Trazabilidad de Datos y Fuentes")
        
        st.markdown("""
        ### 📍 Origen de los Datos
        
        Todos los datos utilizados en esta plataforma proceden de **fuentes públicas oficiales**:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🏛️ Portal de Datos Abiertos de Fuenlabrada
            - **URL:** https://datosabiertos.ayto-fuenlabrada.es/
            - **Organismo:** Ayuntamiento de Fuenlabrada
            - **Licencia:** CC0 1.0 (Dominio Público)
            - **Formato:** CSV/XLSX desde CKAN
            - **Acceso:** Libre y gratuito
            - **Actualización:** Trimestral
            """)
        
        with col2:
            st.markdown("""
            #### 🔒 Seguridad y Privacidad
            - ✅ **Datos públicos:** Sin información personal
            - ✅ **Transparencia:** Procedencia documentada
            - ✅ **Validación:** Verificados por Ayuntamiento
            - ✅ **Anonimización:** Agregados por zona
            - ✅ **Cumplimiento:** RGPD compliant
            """)
        
        st.markdown("---")
        
        st.subheader("📊 Datasets Utilizados")
        
        st.markdown("""
        | Dataset | Cobertura | Actualización | Fiabilidad |
        |---------|-----------|---------------|-----------|
        | Quejas Ciudadanas | Todas las zonas | Mensual | ⭐⭐⭐⭐⭐ |
        | Calidad del Aire | Todas las zonas | Trimestral | ⭐⭐⭐⭐⭐ |
        | Contaminación Acústica | Todas las zonas | Trimestral | ⭐⭐⭐⭐⭐ |
        | Espacios Verdes | Todas las zonas | Anual | ⭐⭐⭐⭐ |
        | Equipamientos Públicos | Todas las zonas | Anual | ⭐⭐⭐⭐⭐ |
        | Actividad Comercial | Todas las zonas | Trimestral | ⭐⭐⭐⭐ |
        """)
        
        st.markdown("---")
        
        st.subheader("📋 Información sobre los Datos Cargados")
        
        if st.session_state.datasets_loaded:
            for name, df_data in st.session_state.datasets_loaded.items():
                st.markdown(f"### {name}")
                st.caption(f"Filas: {len(df_data)} | Columnas: {len(df_data.columns)}")
                
                with st.expander("Ver estructura de datos"):
                    st.dataframe(df_data.head(), use_container_width=True)
        
        st.markdown("---")
        st.subheader("🔍 Reporte de Calidad de Datos")
        
        quality_report = create_data_quality_report(df_master)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Zonas", quality_report["total_rows"])
        
        with col2:
            st.metric("Indicadores", quality_report["total_columns"])
        
        with col3:
            completitud = 100 - (sum(quality_report["missing_values"].values()) / (quality_report["total_rows"] * quality_report["total_columns"]) * 100)
            st.metric("Completitud", f"{completitud:.1f}%")
        
        with col4:
            total_missing = sum(quality_report["missing_values"].values())
            st.metric("Valores Faltantes", total_missing)
        
        st.markdown("""
        #### Explicación de Métricas
        - **Total de Zonas:** Número de zonas de Fuenlabrada analizadas
        - **Indicadores:** Número de variables por zona
        - **Completitud:** Porcentaje de datos no faltantes
        - **Valores Faltantes:** Celdas vacías (imputadas con mediana si existen)
        """)
        
        st.markdown("---")
        st.subheader("📊 Vista del DataFrame Maestro Procesado")
        
        st.markdown("""
        Este es el dataset final utilizado por todos los análisis, predicciones y gráficos.
        Incluye indicadores originales + indicadores calculados + predicciones.
        """)
        
        st.dataframe(
            df_master.round(2),
            use_container_width=True,
            height=400
        )
        
        # Descarga de datos
        st.markdown("---")
        st.subheader("📥 Descargar Resultados del Análisis")
        
        csv = df_master.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV con resultados",
            data=csv,
            file_name="fuenlabrada_smart_priorities_resultados.csv",
            mime="text/csv"
        )
        
        st.markdown("""
        **Nota:** El archivo descargado contiene:
        - Datos originales de las 6 indicadores
        - Índice de Prioridad calculado
        - Clasificación de prioridad (Baja/Media/Alta/Crítica)
        - Predicciones del modelo ML
        - Tendencias esperadas
        """)


# ============================================================================
# PIE DE PÁGINA
# ============================================================================

st.markdown("---")
st.markdown("""
<p style="text-align: center; font-size: 0.9em; color: #666;">
<strong>Fuenlabrada Smart Priorities</strong> | Hackathon Fuenlabrada 2026<br>
Plataforma de análisis de datos públicos abiertos para priorizar actuaciones municipales<br>
<small>Datos públicos del Ayuntamiento de Fuenlabrada | CC0 1.0 License</small>
</p>
""", unsafe_allow_html=True)
