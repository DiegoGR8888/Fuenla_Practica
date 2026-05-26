# 🔧 Guía de Desarrollo

## Estructura de Arquitectura

```
┌─────────────────────────────────────────┐
│         Streamlit Web UI                │
│      (app.py - Interfaz Usuario)        │
└─────────────┬───────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    v         v         v
┌────────┐ ┌────────┐ ┌─────────┐
│ Data   │ │Analysis│ │ Models  │
│ Layer  │ │ Layer  │ │ Layer   │
└────────┘ └────────┘ └─────────┘
    │         │         │
    v         v         v
  Data    Indicators  Predictions
 Loader  + Cleaning   + Recomend.
```

## Módulos y sus Responsabilidades

### 1. **data_loader.py** - Carga de Datos
```python
# Funciones principales:
get_datasets_from_api()              # Conecta API CKAN
download_dataset_from_ckan()         # Descarga dataset
load_uploaded_file()                 # Carga CSV/XLSX
detect_zone_column()                 # Auto-detecta zona
detect_numeric_columns()             # Encuentra números
detect_geo_columns()                 # Encuentra lat/lon
create_sample_data()                 # Datos de demo
load_demo_datasets()                 # Múltiples datasets
```

**Extensión:** Para añadir fuente de datos nueva:
```python
def load_from_postgresql(connection_string):
    # Implementar carga desde PostgreSQL
    pass
```

### 2. **cleaning.py** - Limpieza de Datos
```python
# Funciones principales:
normalize_columns()                  # Nombres columnas
clean_numeric_data()                 # Limpia números
remove_duplicates()                  # Elimina duplicados
handle_missing_values()              # Rellena NaN
normalize_minmax()                   # Normaliza [0,1]
aggregate_by_zone()                  # Agrupa por zona
detect_and_handle_outliers()        # Maneja outliers
merge_datasets()                     # Fusiona DataFrames
create_data_quality_report()        # Reporte calidad
```

**Extensión:** Para estrategia de limpieza personalizada:
```python
def custom_cleaning_strategy(df, strategy_name):
    # Implementar lógica específica
    pass
```

### 3. **indicators.py** - Cálculo de Indicadores
```python
# Funciones principales:
calculate_urban_priority_index()     # Índice principal
calculate_priority_breakdown()       # Desglose
classify_priority()                  # Clasifica
get_priority_color()                 # Color por prioridad
calculate_social_impact_score()      # Impacto social
calculate_environmental_impact_score() # Impacto ambiental
calculate_economic_impact_score()    # Impacto económico
```

**Extensión:** Para modificar ponderaciones:
```python
def calculate_urban_priority_index(df, weights=None):
    if weights is None:
        weights = {
            "quejas": 0.30,           # ← Ajusta aquí
            "contaminacion": 0.20,    # ← Ajusta aquí
            # ...
        }
    # ...
```

### 4. **maps.py** - Visualización Geográfica
```python
# Funciones principales:
create_folium_map()                  # Mapa Folium
create_heatmap()                     # Mapa de calor
plot_priority_distribution_map()     # Por prioridad
create_zone_comparison_map()         # Comparativa
create_pydeck_map()                  # Mapa PyDeck
```

**Extensión:** Para añadir nuevo tipo de mapa:
```python
def create_custom_map(df, custom_config=None):
    # Implementar lógica del mapa
    pass
```

### 5. **model.py** - Machine Learning
```python
# Clase principal:
class PriorityPredictor:
    def __init__()                   # Constructor
    def prepare_features()           # Prepara X
    def train()                      # Entrena modelo
    def predict()                    # Realiza predicciones
    def get_feature_importance()     # Importancia features
    def get_metrics_summary()        # Resumen métricas

# Funciones auxiliares:
calculate_trend()                    # Tendencia
get_risk_level()                     # Nivel riesgo
create_naive_forecast()              # Predicción base
ensemble_predictions()               # Combina modelos
add_predictions_to_df()             # Añade a DataFrame
```

**Extensión:** Para cambiar algoritmo ML:
```python
# En la clase PriorityPredictor.train():
# De: RandomForestRegressor
# A: XGBRegressor, GradientBoostingRegressor, etc.
```

### 6. **recommendations.py** - Recomendaciones
```python
# Clase principal:
class RecommendationEngine:
    @staticmethod
    get_zone_recommendation()        # Reco por zona
    get_top_actions()               # Top 5 acciones
    get_priority_summary()          # Resumen ejecutivo
    get_environmental_focus_areas() # Focos ambientales
    get_social_focus_areas()        # Focos sociales
    get_economic_focus_areas()      # Focos económicos
    generate_comparative_analysis() # Comparativa zonas
```

**Extensión:** Para nuevas reglas de recomendación:
```python
@staticmethod
def get_zone_recommendation(row):
    # Análisis de contaminación
    if row["contaminacion_norm"] > 70:
        # ← Añade nuevas condiciones aquí
```

## Flujo de Ejecución

```
1. Usuario abre app.py
   ↓
2. Carga datos (CSV/XLSX o demo)
   ↓
3. data_loader.py → load_uploaded_file() o create_sample_data()
   ↓
4. cleaning.py → normalize_columns() → clean_numeric_data() → merge_datasets()
   ↓
5. indicators.py → calculate_urban_priority_index()
   ↓
6. model.py → PriorityPredictor.train() → predict()
   ↓
7. recommendations.py → RecommendationEngine.get_zone_recommendation()
   ↓
8. maps.py → Visualizaciones (Folium, Plotly)
   ↓
9. Streamlit renderiza UI → Usuario ve resultados
```

## Personalización Común

### Cambiar el índice de prioridad

**Antes (default):**
```python
weights = {
    "quejas": 0.30,
    "contaminacion": 0.20,
    "ruido": 0.15,
    "zonas_verdes": 0.15,
    "servicios": 0.10,
    "comercio": 0.10,
}
```

**Después (ejemplo - más peso ambiental):**
```python
weights = {
    "quejas": 0.25,
    "contaminacion": 0.30,      # ↑ Aumentado
    "ruido": 0.20,               # ↑ Aumentado
    "zonas_verdes": 0.15,
    "servicios": 0.05,           # ↓ Reducido
    "comercio": 0.05,            # ↓ Reducido
}
```

### Cambiar rangos de clasificación

**Actual:**
```python
bins=[0, 40, 60, 80, 100]
labels=["Baja", "Media", "Alta", "Crítica"]
```

**Personalizado:**
```python
bins=[0, 30, 50, 70, 100]  # Umbrales diferentes
labels=["Verde", "Amarillo", "Naranja", "Rojo"]  # Etiquetas personalizadas
```

### Cambiar paleta de colores

**En indicators.py:**
```python
def get_priority_color(priority: str) -> str:
    colors = {
        "Baja": "#00FF00",      # Verde brillante
        "Media": "#FFFF00",     # Amarillo brillante
        "Alta": "#FF7F00",      # Naranja
        "Crítica": "#FF0000",   # Rojo brillante
    }
    return colors.get(priority, "#808080")
```

## Testing

### Test unitario ejemplo:

```python
# tests/test_indicators.py
import pandas as pd
from src.indicators import calculate_urban_priority_index

def test_priority_index():
    df = pd.DataFrame({
        "zona": ["A", "B"],
        "quejas": [100, 50],
        "contaminacion": [80, 40],
        # ...
    })
    
    result, _ = calculate_urban_priority_index(df)
    
    assert "indice_prioridad" in result.columns
    assert result["indice_prioridad"].min() >= 0
    assert result["indice_prioridad"].max() <= 100
```

## Deploying

### Opción 1: Streamlit Cloud
```bash
# 1. Push a GitHub
git push origin main

# 2. Conecta en https://streamlit.io/cloud
# 3. Selecciona repo y rama
# 4. ¡Listo! Tu app está en internet
```

### Opción 2: Docker
```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

```bash
# Build
docker build -t fuenlabrada-smart .

# Run
docker run -p 8501:8501 fuenlabrada-smart
```

### Opción 3: Heroku
```bash
# 1. Crear Procfile
echo "web: streamlit run app.py" > Procfile

# 2. Deploy
heroku create fuenlabrada-smart
git push heroku main
```

## Debugging

### Activar modo debug en Streamlit

```bash
streamlit run app.py --logger.level=debug
```

### Logs en consola

```python
import streamlit as st
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Esto es un debug message")
logger.info("Info message")
logger.error("Error!")
```

## Performance

### Optimizaciones implementadas:

```python
# 1. Caching de datos
@st.cache_data
def load_initial_data():
    return create_sample_data(), load_demo_datasets()

# 2. Caching de modelos
@st.cache_resource
def get_predictor():
    return PriorityPredictor()

# 3. Limitar renderizaciones
if st.session_state.df_master is not None:
    # Solo actualiza si hay datos
```

### Para mejorar más:

```python
# Usar columnas para paralelismo visual
col1, col2, col3 = st.columns(3)
with col1:
    # Contenido pesado 1
with col2:
    # Contenido pesado 2
with col3:
    # Contenido pesado 3
```

## Contribuciones

1. Fork del repo
2. Crea rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "Añade feature"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## Convenciones de Código

### Nombres de variables
```python
# ✅ Claro
zonas_criticas = df[df["prioridad"] == "Crítica"]
indice_promedio = df["indice_prioridad"].mean()

# ❌ Confuso
zc = df[df["prioridad"] == "Crítica"]
ip = df["indice_prioridad"].mean()
```

### Docstrings
```python
def calculate_urban_priority_index(df: pd.DataFrame, weights: Dict = None) -> Tuple[pd.DataFrame, Dict]:
    """
    Calcula el Índice de Prioridad Urbana
    
    Args:
        df: DataFrame con indicadores por zona
        weights: Ponderaciones por indicador
        
    Returns:
        Tuple: (DataFrame con índice, detalles de cálculo)
    """
    pass
```

## Roadmap Futuro

- [ ] API REST para integración con sistemas municipales
- [ ] Base de datos para histórico de cambios
- [ ] Alertas automáticas cuando zonas cambian de prioridad
- [ ] Análisis de series temporales
- [ ] Simulador interactivo de escenarios
- [ ] Chat/asistente IA para preguntas
- [ ] Exportación a PDF con reportes
- [ ] Integración con portales de participación ciudadana
- [ ] Modelos predictivos más avanzados (LSTM, Prophet)

---

**Happy coding! 🚀**
