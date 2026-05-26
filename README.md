# 📍 Fuenlabrada Smart Priorities

**Plataforma inteligente para priorizar actuaciones urbanas mediante datos abiertos y análisis predictivo**

## 🎯 Objetivo

Convertir datos abiertos y datos municipales en una herramienta visual e inteligente que permita a Fuenlabrada:
- 🗺️ Identificar zonas que requieren atención prioritaria
- 📊 Analizar múltiples indicadores (social, ambiental, económico)
- 🤖 Predecir problemas futuros con Machine Learning
- 💡 Generar recomendaciones automáticas de actuación

## 🚀 Características Principales

### 📍 Mapa Interactivo
- Visualización geográfica de zonas por nivel de prioridad
- Diferentes tipos de mapas: puntos, heatmap, por prioridad
- Información detallada al hacer clic en cada zona

### ⭐ Índice de Prioridad Urbana
- Puntuación de 0-100 que combina 6 indicadores
- Clasificación: Baja, Media, Alta, Crítica
- Desglose de contribución de cada componente

### 🌳 Análisis Ambiental
- Evaluación de contaminación, ruido y zonas verdes
- Identificación de puntos críticos ambientales
- Recomendaciones de intervención verde

### 🤖 Predicción con ML
- Modelo Random Forest para estimar prioridades futuras
- Detección de tendencias (mejora/empeora)
- Análisis de importancia de features

### 🧠 Recomendaciones Automáticas
- Generadas según análisis de datos por zona
- Top acciones municipales recomendadas
- Priorizadas por eje de impacto (social, ambiental, económico)

### 📊 Dashboard Completo
- Métricas principales en tiempo real
- Gráficos interactivos con Plotly
- Análisis de tres ejes de impacto

### 📦 Trazabilidad de Datos
- Documentación de fuentes utilizadas
- Reporte de calidad de datos
- Descarga de resultados en CSV

## 📋 Indicadores Utilizados

El Índice de Prioridad Urbana se calcula con las siguientes ponderaciones:

| Indicador | Peso | Descripción |
|-----------|------|-------------|
| Quejas/Incidencias | 30% | Problemas reportados por ciudadanía |
| Contaminación | 20% | Calidad del aire, PM10, PM2.5, NO2 |
| Ruido | 15% | Contaminación acústica en dB |
| Zonas Verdes | 15% | Déficit de espacios verdes por habitante |
| Servicios Públicos | 10% | Cobertura de salud, educación, etc. |
| Actividad Comercial | 10% | Dinamismo económico local |

## 🛠️ Requisitos

- Python 3.8+
- pip o conda

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd fuenlabrada-smart-priorities
```

### 2. Crear entorno virtual (recomendado)
```bash
# Con venv
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# O con conda
conda create -n fuenlabrada python=3.9
conda activate fuenlabrada
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🚀 Ejecución

### Ejecutar la aplicación
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

### Opciones
```bash
# Con puerto específico
streamlit run app.py --server.port 8080

# Modo headless
streamlit run app.py --logger.level=error
```

## 📁 Estructura del Proyecto

```
fuenlabrada-smart-priorities/
├── app.py                      # Aplicación principal Streamlit
├── requirements.txt            # Dependencias Python
├── README.md                   # Este archivo
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Carga de datos (API, CSV, XLSX)
│   ├── cleaning.py            # Limpieza y normalización
│   ├── indicators.py          # Cálculo de índices
│   ├── maps.py                # Visualización geográfica
│   ├── model.py               # Modelo predictivo ML
│   └── recommendations.py     # Motor de recomendaciones
│
├── data/
│   ├── raw/                   # Datos sin procesar
│   └── processed/             # Datos procesados
│
└── notebooks/
    └── exploracion.ipynb      # Análisis exploratorio
```

## 💾 Dependencias Principales

```
streamlit              1.28.1    # Framework web
pandas                 2.1.1     # Análisis de datos
numpy                  1.24.3    # Cálculos numéricos
plotly                 5.17.0    # Gráficos interactivos
scikit-learn           1.3.1     # Machine Learning
folium                 0.14.0    # Mapas Leaflet
geopandas              0.13.2    # Datos geoespaciales
requests               2.31.0    # Llamadas HTTP/API
openpyxl               3.11.0    # Lectura XLSX
```

## 📊 Cómo Usar

### 1. Cargar Datos

**Opción A: Datos de Demostración**
- Selecciona "Usar datos de demostración" en el sidebar
- Se cargarán automáticamente datos de ejemplo para Fuenlabrada

**Opción B: Cargar tu CSV/XLSX**
- Haz clic en "Cargar CSV/XLSX"
- Sube tu archivo
- La app detectará automáticamente zonas y coordenadas

### 2. Explorar Resultados

Navega por las pestañas:
- **🏙️ Inicio**: Resumen ejecutivo
- **📍 Mapa**: Visualización geográfica
- **⭐ Índice**: Ranking de prioridades
- **🌳 Ambiente**: Análisis ambiental
- **🤖 Predicción**: Modelo ML
- **🧠 Recomendaciones**: Acciones sugeridas
- **📦 Datos**: Trazabilidad

### 3. Analizar por Zona

En la pestaña de Recomendaciones:
- Selecciona una zona del dropdown
- Visualiza su puntuación detallada
- Lee recomendaciones personalizadas

### 4. Descargar Resultados

Usa el botón "Descargar CSV" en la pestaña Datos para exportar:
- Todas las zonas analizadas
- Índices calculados
- Predicciones
- Recomendaciones

## 🤖 Modelo Predictivo

El modelo predictivo utiliza:

**Algoritmo:** Random Forest Regressor
- 100 árboles de decisión
- Profundidad máxima: 10
- Validación: Train/Test 80/20

**Variables de entrada:**
- Quejas normalizadas
- Contaminación normalizada
- Ruido normalizado
- Zonas verdes normalizado
- Servicios públicos normalizados
- Actividad comercial normalizada

**Salida:**
- Índice de prioridad predicho (0-100)
- Tendencia (mejora/empeora/estable)
- Nivel de riesgo futuro

**Nota:** El modelo mejora automáticamente con más datos históricos.

## 📈 Metodología

### 1. Carga de Datos
- Desde portal de datos abiertos (API CKAN)
- Desde archivos locales (CSV, XLSX)
- Detección automática de columnas

### 2. Limpieza y Preparación
- Normalización de nombres de columnas
- Tratamiento de valores faltantes
- Detección y manejo de outliers
- Validación de datos geográficos

### 3. Cálculo de Índices
- Normalización Min-Max [0, 1] de indicadores
- Ponderación según importancia
- Agregación por zona
- Clasificación (Baja/Media/Alta/Crítica)

### 4. Análisis Predictivo
- Entrenamiento de modelo ML
- Generación de predicciones
- Cálculo de tendencias

### 5. Generación de Recomendaciones
- Análisis de umbrales por indicador
- Generación automática de texto
- Priorización de acciones

## 🔍 Validación de Datos

La aplicación incluye verificación de:
- ✅ Valores numéricos válidos
- ✅ Coordenadas geográficas (latitud/longitud)
- ✅ Nombres de zona consistentes
- ✅ Rango de valores esperados [0-100]
- ✅ Completitud de datos (% valores presentes)

## 🎨 Paleta de Colores

```
Prioridad Baja    → Verde (#28a745)
Prioridad Media   → Amarillo (#ffc107)
Prioridad Alta    → Naranja (#fd7e14)
Prioridad Crítica → Rojo (#dc3545)
```

## 📝 Ejemplos de Datos

### CSV mínimo requerido:
```csv
zona,quejas,contaminacion,ruido,zonas_verdes,servicios_publicos,actividad_comercial
Centro,342,85.5,78.2,12.3,8,156
El Naranjo,298,72.3,71.8,18.5,6,142
Loranca,245,65.2,68.9,22.1,5,134
```

### Con coordenadas (opcional pero recomendado):
```csv
zona,quejas,contaminacion,ruido,zonas_verdes,servicios_publicos,actividad_comercial,latitud,longitud
Centro,342,85.5,78.2,12.3,8,156,40.3210,-3.8045
El Naranjo,298,72.3,71.8,18.5,6,142,40.3215,-3.8052
```

## 🐛 Troubleshooting

### "No hay suficientes datos para entrenar"
- Se necesitan al menos 5 zonas
- Carga más datos o usa datos de demostración

### "No hay coordenadas geográficas"
- Añade columnas de latitud y longitud
- La app las detectará automáticamente
- Nombres de columnas: "lat", "latitude", "lon", "longitude"

### Error de módulos importados
```bash
# Reinstala dependencias
pip install --upgrade -r requirements.txt
```

### Puerto 8501 en uso
```bash
streamlit run app.py --server.port 8080
```

## 🔐 Privacidad y Seguridad

- Todos los datos procesados localmente
- No se envía información a servidores externos
- Los datos cargados se procesan en sesión
- Descarga de resultados solo en tu máquina

## 📚 Documentación Técnica

### Flujo de Datos
```
Input (CSV/XLSX)
    ↓
Normalización
    ↓
Limpieza
    ↓
Detección de columnas
    ↓
Cálculo de Índices
    ↓
Entrenamiento ML
    ↓
Predicciones
    ↓
Recomendaciones
    ↓
Visualización
```

### Clases Principales

**data_loader.py**
- `get_datasets_from_api()`: Conecta con API CKAN
- `download_dataset_from_ckan()`: Descarga dataset específico
- `load_uploaded_file()`: Carga archivos subidos
- `detect_zone_column()`: Auto-detección de columna de zona

**cleaning.py**
- `normalize_columns()`: Normaliza nombres
- `clean_numeric_data()`: Limpia números
- `merge_datasets()`: Fusiona múltiples DataFrames

**indicators.py**
- `calculate_urban_priority_index()`: Calcula índice principal
- `calculate_social_impact_score()`: Impacto social
- `calculate_environmental_impact_score()`: Impacto ambiental
- `calculate_economic_impact_score()`: Impacto económico

**model.py**
- `PriorityPredictor`: Clase principal del modelo
- `.train()`: Entrena Random Forest
- `.predict()`: Realiza predicciones
- `.get_feature_importance()`: Importancia de features

**recommendations.py**
- `RecommendationEngine`: Motor de recomendaciones
- `get_zone_recommendation()`: Recomendación por zona
- `get_top_actions()`: Top acciones municipales

## 🌐 Integración con API CKAN

La aplicación puede conectarse con el Portal de Datos Abiertos de Fuenlabrada:

```python
from src.data_loader import download_dataset_from_ckan

# Ejemplo: Descargar dataset de calidad del aire
df_aire = download_dataset_from_ckan("calidad-del-aire")
```

## 📊 Exportación de Reportes

La aplicación permite descargar:
- **CSV**: Resultados completos
- **Visualizaciones**: Captura de pantalla desde navegador
- **Mapas**: Exportar como HTML desde el mapa Folium

## 🚀 Mejoras Futuras

- [ ] Exportación a PDF
- [ ] Comparativa de escenarios
- [ ] Simulador interactivo de pesos
- [ ] Chat explicativo con IA
- [ ] API REST para integración
- [ ] Base de datos para histórico
- [ ] Alertas automáticas por cambios
- [ ] Análisis de series temporales

## 📄 Licencia

Este proyecto se desarrolló para el DATA-HACK-FUENLABRADA 2026.

## ✉️ Contacto

Para dudas sobre el proyecto:
- Email: data-hack-fuenlabrada2026@ayto-fuenlabrada.es

## 🙏 Agradecimientos

Datos facilitados por:
- Ayuntamiento de Fuenlabrada
- Portal de Datos Abiertos de Fuenlabrada
- Comunidad Open Data de Madrid

---

**Última actualización:** Mayo 2026
**Versión:** 1.0
