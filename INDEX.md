# 📑 Índice de Archivos del Proyecto

## 📂 Estructura Completa

```
fuenlabrada-smart-priorities/
│
├── 📄 app.py                       ← APLICACIÓN PRINCIPAL (Streamlit)
├── 📄 requirements.txt             ← Dependencias Python
├── 📄 README.md                    ← Documentación completa
├── 📄 QUICK_START.md               ← Guía rápida de inicio
├── 📄 DEVELOPMENT.md               ← Guía de desarrollo y extensión
├── 📄 INDEX.md                     ← Este archivo
├── 📄 .gitignore                   ← Archivos ignorados en Git
│
├── .streamlit/
│   └── config.toml                 ← Configuración Streamlit
│
├── src/                            ← MÓDULOS PRINCIPALES
│   ├── __init__.py                 ← Inicializador del paquete
│   ├── data_loader.py              ← Carga de datos (API CKAN, CSV, XLSX)
│   ├── cleaning.py                 ← Limpieza y preparación de datos
│   ├── indicators.py               ← Cálculo de índices de prioridad
│   ├── maps.py                     ← Visualización geográfica (Folium, PyDeck)
│   ├── model.py                    ← Modelo predictivo (Random Forest)
│   └── recommendations.py          ← Motor de recomendaciones automáticas
│
├── data/
│   ├── raw/                        ← Datos sin procesar
│   │   └── ejemplo_fuenlabrada.csv ← Archivo de ejemplo
│   └── processed/                  ← Datos procesados
│
└── notebooks/
    └── exploracion.ipynb           ← Análisis exploratorio (Jupyter)
```

## 📄 Descripción de Archivos Principales

### 🎯 app.py (1200+ líneas)
**Aplicación principal en Streamlit**

- Interfaz web completa
- 7 pestañas de análisis
- Gestión de estado con session_state
- Visualización de datos con Plotly
- Integración de todos los módulos

**Contiene:**
- Layout y configuración de página
- Funciones de UI (métricas, ranking, gráficos)
- Lógica de procesamiento de datos
- Navegación entre pestañas

---

### 📦 requirements.txt
**Dependencias del proyecto**

```
streamlit==1.28.1
pandas==2.1.1
numpy==1.24.3
plotly==5.17.0
scikit-learn==1.3.1
folium==0.14.0
streamlit-folium==0.15.0
requests==2.31.0
openpyxl==3.11.0
geopandas==0.13.2
```

**Instalación:**
```bash
pip install -r requirements.txt
```

---

### 📚 README.md
**Documentación completa del proyecto (800+ líneas)**

Contiene:
- Descripción del proyecto
- Características principales
- Guía de instalación
- Cómo usar la aplicación
- Metodología
- Estructura del proyecto
- Troubleshooting
- Licencia

**Audiencia:** Usuarios finales, stakeholders, jurado

---

### 🚀 QUICK_START.md
**Guía rápida de 3 pasos (300+ líneas)**

Contiene:
- Instalación en 3 pasos
- Primer uso con datos de demo
- Cómo cargar datos propios
- Troubleshooting rápido
- Preguntas frecuentes

**Audiencia:** Usuarios nuevos que necesitan empezar rápido

---

### 🔧 DEVELOPMENT.md
**Guía para desarrolladores (600+ líneas)**

Contiene:
- Arquitectura del sistema
- Responsabilidades de cada módulo
- Flujo de ejecución
- Cómo personalizar (pesos, colores, etc.)
- Testing
- Deploy (Docker, Streamlit Cloud, Heroku)
- Debugging
- Convenciones de código

**Audiencia:** Desarrolladores que quieren extender el proyecto

---

## 🔌 Módulos src/

### data_loader.py (300+ líneas)
**Responsabilidad:** Carga de datos desde múltiples fuentes

**Funciones principales:**
- `get_datasets_from_api()` - Conecta con API CKAN
- `download_dataset_from_ckan()` - Descarga dataset
- `load_uploaded_file()` - Carga CSV/XLSX
- `detect_zone_column()` - Auto-detecta columna de zona
- `create_sample_data()` - Datos de demostración
- `load_demo_datasets()` - Múltiples datasets de demo

**Cómo extender:**
- Añadir nuevas fuentes de datos (PostgreSQL, API REST, etc.)
- Mejorar auto-detección de columnas

---

### cleaning.py (400+ líneas)
**Responsabilidad:** Limpieza y preparación de datos

**Funciones principales:**
- `normalize_columns()` - Normaliza nombres de columnas
- `clean_numeric_data()` - Limpia valores numéricos
- `handle_missing_values()` - Rellena NaN
- `normalize_minmax()` - Normaliza a [0,1]
- `merge_datasets()` - Fusiona DataFrames
- `detect_and_handle_outliers()` - Maneja outliers

**Cómo extender:**
- Estrategias de limpieza personalizadas
- Validación de datos específica

---

### indicators.py (600+ líneas)
**Responsabilidad:** Cálculo de índices de prioridad

**Funciones principales:**
- `calculate_urban_priority_index()` - Índice principal (6 indicadores)
- `calculate_social_impact_score()` - Impacto social
- `calculate_environmental_impact_score()` - Impacto ambiental
- `calculate_economic_impact_score()` - Impacto económico

**Fórmula del índice:**
```
Índice = (30% Quejas + 20% Contaminación + 15% Ruido + 
          15% Zonas Verdes + 10% Servicios + 10% Comercio)
```

**Cómo personalizar:**
- Cambiar pesos de indicadores
- Cambiar rangos de clasificación (Baja/Media/Alta/Crítica)
- Añadir nuevos indicadores

---

### maps.py (500+ líneas)
**Responsabilidad:** Visualización geográfica

**Funciones principales:**
- `create_folium_map()` - Mapa interactivo con puntos
- `create_heatmap()` - Mapa de calor
- `plot_priority_distribution_map()` - Mapa por prioridad
- `create_zone_comparison_map()` - Mapa comparativo
- `create_pydeck_map()` - Visualización 3D

**Características:**
- Mapas interactivos con Folium
- Popup con información detallada
- Control de capas
- Colores dinámicos según prioridad

---

### model.py (500+ líneas)
**Responsabilidad:** Machine Learning predictivo

**Clase principal:**
```python
class PriorityPredictor:
    def train()              # Entrena Random Forest
    def predict()            # Realiza predicciones
    def get_feature_importance()  # Importancia de features
```

**Algoritmo:** Random Forest Regressor
- 100 estimadores
- Profundidad máxima 10
- Split train/test 80/20

**Características:**
- Ensemble de predicciones (ML + naive)
- Cálculo de tendencias
- Métricas de evaluación (R², RMSE, MAE)

**Cómo extender:**
- Cambiar a otro algoritmo (XGBoost, LightGBM, etc.)
- Añadir validación cruzada
- Tuning de hiperparámetros

---

### recommendations.py (400+ líneas)
**Responsabilidad:** Generación automática de recomendaciones

**Clase principal:**
```python
class RecommendationEngine:
    get_zone_recommendation()    # Reco por zona
    get_top_actions()           # Top 5 acciones
    get_environmental_focus_areas()  # Zonas ambientales
    get_social_focus_areas()    # Zonas sociales
    get_economic_focus_areas()  # Zonas económicas
```

**Características:**
- Reglas basadas en umbrales
- Generación de texto automático
- Priorización de acciones
- Análisis comparativo entre zonas

---

## 📋 Configuración

### .streamlit/config.toml
**Configuración de Streamlit**

```toml
[theme]
primaryColor = "#003366"        # Color principal
backgroundColor = "#f5f5f5"     # Fondo
secondaryBackgroundColor = "#e8e8e8"

[server]
port = 8501
maxUploadSize = 200
```

---

## 📊 Datos

### data/raw/ejemplo_fuenlabrada.csv
**Dataset de ejemplo con 15 zonas de Fuenlabrada**

Columnas:
- zona: Nombre de zona
- quejas: Número de quejas
- contaminacion: Índice de contaminación
- ruido: Nivel de ruido en dB
- zonas_verdes: Hectáreas de zonas verdes
- servicios_publicos: Número de servicios
- actividad_comercial: Número de comercios
- poblacion: Número de habitantes
- latitud: Coordenada lat
- longitud: Coordenada lon

**Uso:** Para pruebas y demostración

---

## 📝 Documentación

| Archivo | Audiencia | Contenido |
|---------|-----------|----------|
| README.md | Usuarios, Jurado | Qué es, características, cómo usar |
| QUICK_START.md | Usuarios nuevos | Empezar en 5 minutos |
| DEVELOPMENT.md | Desarrolladores | Cómo extender y personalizar |
| INDEX.md | Este archivo | Guía de todos los archivos |

---

## 🚀 Flujo de Uso

```
Usuario abre app.py
    ↓
Selecciona datos (demo o upload)
    ↓
data_loader.py → Carga datos
    ↓
cleaning.py → Limpia y normaliza
    ↓
indicators.py → Calcula índices
    ↓
model.py → Entrena y predice
    ↓
recommendations.py → Genera recomendaciones
    ↓
maps.py → Visualiza en mapas
    ↓
Streamlit renderiza UI
    ↓
Usuario ve 7 pestañas de análisis
```

---

## 📊 Estadísticas del Código

| Componente | Líneas | Complejidad |
|-----------|--------|------------|
| app.py | 1200+ | Alta (interfaz) |
| data_loader.py | 300+ | Media |
| cleaning.py | 400+ | Media |
| indicators.py | 600+ | Media-Alta |
| maps.py | 500+ | Alta (gráficos) |
| model.py | 500+ | Media-Alta (ML) |
| recommendations.py | 400+ | Media |
| **Total** | **3900+** | **Robusto** |

---

## 🔄 Versionado

**Versión actual:** 1.0
**Fecha de creación:** Mayo 2026
**Estado:** Completo y funcional

---

## 📞 Soporte

Para dudas sobre:
- **Uso de la app:** Ver QUICK_START.md
- **Cómo funciona:** Ver README.md
- **Desarrollo/extensión:** Ver DEVELOPMENT.md
- **Estructura de archivos:** Ver este INDEX.md

---

## ✅ Checklist de Archivos

```
[✅] app.py                      - Aplicación principal
[✅] requirements.txt            - Dependencias
[✅] README.md                   - Documentación
[✅] QUICK_START.md              - Guía rápida
[✅] DEVELOPMENT.md              - Guía desarrollador
[✅] INDEX.md                    - Este archivo
[✅] .gitignore                  - Config Git
[✅] .streamlit/config.toml      - Config Streamlit
[✅] src/data_loader.py          - Carga datos
[✅] src/cleaning.py             - Limpieza
[✅] src/indicators.py           - Indicadores
[✅] src/maps.py                 - Mapas
[✅] src/model.py                - ML
[✅] src/recommendations.py      - Recomendaciones
[✅] src/__init__.py             - Init
[✅] data/raw/ejemplo_fuenlabrada.csv - Datos ejemplo
[✅] notebooks/exploracion.ipynb - Notebook
```

---

**¡Proyecto completamente documentado y listo para usar! 🚀**

Para empezar inmediatamente, ve a QUICK_START.md
