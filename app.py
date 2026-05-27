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
    """Muestra análisis ambiental detallado"""
    
    st.subheader("🌳 Análisis Ambiental Detallado")
    
    col1, col2 = st.columns(2)
    
    # Contaminación
    with col1:
        if "contaminacion_norm" in df.columns:
            st.write("**Contaminación por Zona**")
            df_sorted = df.nlargest(10, "contaminacion_norm")[["zona", "contaminacion_norm"]]
            
            fig = px.bar(
                df_sorted,
                x="contaminacion_norm",
                y="zona",
                orientation="h",
                color="contaminacion_norm",
                color_continuous_scale="Reds",
                title="Zonas con Mayor Contaminación"
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Ruido
    with col2:
        if "ruido_norm" in df.columns:
            st.write("**Contaminación Acústica por Zona**")
            df_sorted = df.nlargest(10, "ruido_norm")[["zona", "ruido_norm"]]
            
            fig = px.bar(
                df_sorted,
                x="ruido_norm",
                y="zona",
                orientation="h",
                color="ruido_norm",
                color_continuous_scale="Oranges",
                title="Zonas con Mayor Ruido"
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Zonas verdes
    st.write("**Déficit de Zonas Verdes (Mayor necesidad)**")
    if "zonas_verdes_norm" in df.columns:
        df_sorted = df.nlargest(10, "zonas_verdes_norm")[["zona", "zonas_verdes_norm"]]
        
        fig = px.bar(
            df_sorted,
            x="zonas_verdes_norm",
            y="zona",
            orientation="h",
            color="zonas_verdes_norm",
            color_continuous_scale="Greens_r",
            title="Zonas con Mayor Déficit Verde"
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
# SIDEBAR - CARGA DE DATOS
# ============================================================================

st.sidebar.markdown("# 📦 Gestión de Datos")

st.sidebar.markdown("### Opciones de carga:")

data_option = st.sidebar.radio(
    "Selecciona opción:",
    ["📂 Cargar CSV/XLSX", "🎲 Usar datos de demostración"]
)

if data_option == "📂 Cargar CSV/XLSX":
    st.sidebar.markdown("#### Sube tu dataset")
    uploaded_file = st.sidebar.file_uploader(
        "Selecciona CSV o XLSX",
        type=["csv", "xlsx"],
        key="file_uploader"
    )
    
    if uploaded_file:
        df = load_uploaded_file(uploaded_file)
        if df is not None:
            st.session_state.datasets_loaded[uploaded_file.name] = df
            st.session_state.df_master = df
            st.sidebar.success(f"✅ Cargado: {uploaded_file.name}")
else:
    # Carga datos de demostración
    df, demo_datasets = load_initial_data()
    st.session_state.df_master = df
    st.session_state.datasets_loaded = demo_datasets
    st.sidebar.success("✅ Datos de demostración cargados")


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
        
        # Información general
        col1, col2, col3, col4 = st.columns(4)
        
        summary = RecommendationEngine.get_priority_summary(df_master)
        
        with col1:
            st.metric("Total de Zonas", summary["total_zonas"])
        with col2:
            st.metric("Promedio de Índice", f"{summary['indice_promedio']:.1f}")
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
                title="Distribución de Zonas por Prioridad",
                color_discrete_map={
                    "Crítica": "#dc3545",
                    "Alta": "#fd7e14",
                    "Media": "#ffc107",
                    "Baja": "#28a745"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Información de Zonas")
            st.markdown(f"""
            - **Zona más crítica**: {summary['peor_zona']} (Índice: {df_master[df_master['zona']==summary['peor_zona']]['indice_prioridad'].values[0]:.1f})
            - **Zona en mejor estado**: {summary['mejor_zona']} (Índice: {df_master[df_master['zona']==summary['mejor_zona']]['indice_prioridad'].values[0]:.1f})
            - **Diferencia máxima**: {df_master['indice_prioridad'].max() - df_master['indice_prioridad'].min():.1f} puntos
            """)
        
        st.markdown("---")
        display_indicators_dashboard(df_master)
    
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
        El Índice de Prioridad Urbana combina múltiples indicadores para evaluar
        la necesidad de intervención municipal en cada zona.
        
        **Ponderaciones:**
        - 30% Quejas/Incidencias ciudadanas
        - 20% Contaminación ambiental
        - 15% Contaminación acústica (Ruido)
        - 15% Déficit de zonas verdes
        - 10% Falta de servicios públicos
        - 10% Baja actividad comercial
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            display_priority_ranking(df_master, top_n=15)
        
        with col2:
            st.markdown("### Clasificación")
            st.markdown("""
            - 🟢 **Baja** (0-40)
            - 🟡 **Media** (40-60)
            - 🟠 **Alta** (60-80)
            - 🔴 **Crítica** (80-100)
            """)
            
            st.markdown("### Estadísticas")
            st.metric("Máximo", f"{df_master['indice_prioridad'].max():.1f}")
            st.metric("Mínimo", f"{df_master['indice_prioridad'].min():.1f}")
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
        
        if st.session_state.model_trained:
            st.markdown("""
            Se ha entrenado un modelo de **Random Forest** para predecir
            la evolución del índice de prioridad en las próximas evaluaciones.
            """)
            
            st.info(st.session_state.predictor.get_metrics_summary())
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Importancia de Features")
                feature_importance = st.session_state.predictor.get_feature_importance()
                if not feature_importance.empty:
                    fig = px.bar(
                        feature_importance,
                        x="importance",
                        y="feature",
                        orientation="h",
                        title="Importancia de Indicadores",
                        labels={"importance": "Importancia", "feature": "Indicador"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Predicción vs Actual")
                if "prediccion_prioridad" in df_master.columns:
                    df_pred = df_master[["zona", "indice_prioridad", "prediccion_prioridad"]].copy()
                    df_pred["diferencia"] = df_pred["prediccion_prioridad"] - df_pred["indice_prioridad"]
                    df_pred_top = df_pred.nlargest(10, "diferencia")
                    
                    fig = go.Figure(data=[
                        go.Bar(name="Actual", x=df_pred_top["zona"], y=df_pred_top["indice_prioridad"]),
                        go.Bar(name="Predicción", x=df_pred_top["zona"], y=df_pred_top["prediccion_prioridad"])
                    ])
                    fig.update_layout(title="Top 10 Zonas: Actual vs Predicción", height=400)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de predicciones
            st.subheader("📊 Predicciones Detalladas")
            if "prediccion_prioridad" in df_master.columns and "tendencia" in df_master.columns:
                pred_table = df_master[[
                    "zona", "indice_prioridad", "prediccion_prioridad", "tendencia", "riesgo_futuro"
                ]].copy()
                pred_table["diferencia"] = pred_table["prediccion_prioridad"] - pred_table["indice_prioridad"]
                pred_table = pred_table.sort_values("prediccion_prioridad", ascending=False)
                
                st.dataframe(
                    pred_table.round(2),
                    use_container_width=True,
                    hide_index=True
                )
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
        st.markdown("## 📦 Trazabilidad de Datos")
        
        st.subheader("📊 Datasets Cargados")
        
        if st.session_state.datasets_loaded:
            for name, df_data in st.session_state.datasets_loaded.items():
                st.markdown(f"### {name}")
                st.caption(f"Filas: {len(df_data)} | Columnas: {len(df_data.columns)}")
                
                with st.expander("Ver estructura"):
                    st.dataframe(df_data.head(), use_container_width=True)
        
        st.markdown("---")
        st.subheader("🔍 Reporte de Calidad de Datos")
        
        quality_report = create_data_quality_report(df_master)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Filas", quality_report["total_rows"])
        
        with col2:
            st.metric("Total de Columnas", quality_report["total_columns"])
        
        with col3:
            total_missing = sum(quality_report["missing_values"].values())
            st.metric("Valores Faltantes", total_missing)
        
        st.markdown("---")
        
        st.subheader("📋 DataFrame Maestro")
        st.dataframe(
            df_master.round(2),
            use_container_width=True,
            height=400
        )
        
        # Descarga de datos
        st.markdown("---")
        st.subheader("📥 Descargar Resultados")
        
        csv = df_master.to_csv(index=False)
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="fuenlabrada_smart_priorities_resultados.csv",
            mime="text/csv"
        )


# ============================================================================
# PIE DE PÁGINA
# ============================================================================

st.markdown("---")
st.markdown("""
<p style="text-align: center; font-size: 0.9em; color: #666;">
<strong>Fuenlabrada Smart Priorities</strong> | DATA-HACK-FUENLABRADA 2026<br>
Plataforma de análisis de datos abiertos para priorizar actuaciones municipales
</p>
""", unsafe_allow_html=True)
