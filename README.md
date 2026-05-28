# 📍 Fuenlabrada Smart Priorities

**Plataforma inteligente para priorizar actuaciones urbanas mediante datos abiertos y análisis predictivo**

---

## 🎯 Objetivo

Convertir datos abiertos y datos municipales en una herramienta visual e inteligente que permita al Ayuntamiento de Fuenlabrada:

- 🗺️ **Identificar zonas críticas** que requieren atención prioritaria
- 📊 **Analizar múltiples indicadores** (social, ambiental, económico)
- 🤖 **Predecir problemas futuros** con Machine Learning
- 💡 **Generar recomendaciones** automáticas de actuación
- 🌍 **Utilizar datos públicos** del portal abierto de Fuenlabrada

---

## 🚀 Características Principales

### 1. **📍 Mapa Interactivo de Prioridades**
- Visualización geográfica de zonas coloreadas por nivel de prioridad
- Sistema de colores intuitivo:
  - 🟢 Verde: Prioridad baja (0-40)
  - 🟡 Amarillo: Prioridad media (40-60)
  - 🟠 Naranja: Prioridad alta (60-80)
  - 🔴 Rojo: Prioridad crítica (80-100)
- Información detallada al hacer clic en cada zona
- Múltiples tipos de vista: puntos, heatmap, por prioridad

### 2. **⭐ Índice de Prioridad Urbana**
- Puntuación única de 0-100 que combina 6 indicadores clave
- **Fórmula ponderada:**
  - 30% Quejas/Incidencias ciudadanas
  - 20% Contaminación ambiental
  - 15% Contaminación acústica (Ruido)
  - 15% Déficit de zonas verdes
  - 10% Falta de servicios públicos
  - 10% Baja actividad comercial
- Ranking ordenado por prioridad
- Explicabilidad total del índice

### 3. **🌳 Análisis Ambiental**
- Evaluación de contaminación del aire, ruido y zonas verdes
- Relación entre contaminación y espacios verdes
- Ranking de zonas por déficit ambiental
- Recomendaciones de intervención verde

### 4. **🤖 Predicción con Machine Learning**
- Modelo **Random Forest Regressor** para estimar prioridades futuras
- Detección de tendencias (mejora/empeora/estable)
- Análisis de importancia de features
- Error y métricas de validación del modelo
- Alerta de riesgo futuro por zona

### 5. **🧠 Recomendaciones Automáticas**
- Generadas según análisis de datos por zona
- Top 5 acciones municipales recomendadas
- Recomendaciones específicas por eje:
  - 👥 **Social**: Atención ciudadana, servicios
  - 🌳 **Ambiental**: Reducción contaminación, zonas verdes
  - 💰 **Económico**: Actividad comercial, emprendimiento

### 6. **📊 Dashboard Ejecutivo**
- Métricas principales en tiempo real
- Distribución de zonas por prioridad (gráfico de pastel)
- Impacto por eje (social, ambiental, económico)
- Visualizaciones interactivas con Plotly

### 7. **📦 Trazabilidad de Datos**
- Documentación completa de fuentes utilizadas
- Reporte de calidad de datos
- Detalle de datasets cargados
- Descarga de resultados en CSV

---

## 📊 Indicadores Utilizados y Definiciones

### Fuente Principal de Datos
**Portal de Datos Abiertos del Ayuntamiento de Fuenlabrada**
- URL: https://datosabiertos.ayto-fuenlabrada.es/
- Formato: CSV/XLSX desde CKAN
- Licencia: CC0 1.0 (Dominio Público)
- Cobertura: Todas las zonas de Fuenlabrada
- Actualización: Trimestral

### 6 Indicadores Clave del Índice

#### 1️⃣ **Quejas Ciudadanas (Peso: 30%)**
| Aspecto | Detalle |
|---------|---------|
| **Qué mide** | Número de incidencias/reclamaciones ciudadanas |
| **Rango** | 0-500+ quejas por período |
| **Interpretación** | Mayor número = Mayor insatisfacción ciudadana |
| **Fuente** | Plataforma de Participación Ciudadana - Ayto Fuenlabrada |
| **Significado** | Refleja problemas percibidos por los habitantes |
| **Problemas captados** | Servicios deficientes, limpieza, seguridad, ruido |

#### 2️⃣ **Contaminación del Aire (Peso: 20%)**
| Aspecto | Detalle |
|---------|---------|
| **Qué mide** | Concentración de PM2.5 y NO₂ en μg/m³ |
| **Rango** | 0-100 (Bueno a Peligroso según OMS) |
| **Interpretación** | >35 μg/m³ indica aire insalubre |
| **Fuente** | Red de Monitoreo Ambiental Municipal |
| **Significado** | Impacto directo en salud respiratoria |
| **Problemas captados** | Tráfico vehicular, industria, calefacción |

#### 3️⃣ **Contaminación Acústica (Peso: 15%)**
| Aspecto | Detalle |
|---------|---------|
| **Qué mide** | Nivel de ruido ambiental en dB (decibelios) |
| **Rango** | 55-85 dB |
| **Interpretación** | >70dB afecta sueño y concentración (OMS) |
| **Fuente** | Red de Monitoreo Acústico - CKAN Municipal |
| **Significado** | Afecta calidad de vida y bienestar |
| **Problemas captados** | Tráfico, comercios, vida nocturna, construcción |

#### 4️⃣ **Déficit de Zonas Verdes (Peso: 15%)**
| Aspecto | Detalle |
|---------|---------|
| **Qué mide** | m² de parques/espacios verdes por habitante |
| **Rango** | 0-50+ m²/hab (Inverso: menos verde = más prioridad) |
| **Interpretación** | <9 m²/hab es insuficiente según ONU |
| **Fuente** | Inventario Municipal de Espacios Públicos |
| **Significado** | Necesidad de espacios para ocio y regulación climática |
| **Problemas captados** | Falta de parques, plazas, arbolado urbano |

#### 5️⃣ **Equipamientos Públicos (Peso: 10%)**
| Aspecto | Detalle |
|---------|---------|
| **Qué mide** | Disponibilidad de servicios (centros salud, educación, etc.) |
| **Rango** | Número de equipamientos por zona |
| **Interpretación** | Menor disponibilidad = Mayor necesidad |
| **Fuente** | Catálogo Municipal de Servicios Públicos |
| **Significado** | Acceso a servicios básicos de calidad |
| **Problemas captados** | Déficit de colegios, ambulatorios, centros cívicos |

#### 6️⃣ **Actividad Comercial (Peso: 10%)**
| Aspecto | Detalle |
|---------|---------|
| **Qué mide** | Número de comercios activos |
| **Rango** | 0-400+ comercios por zona |
| **Interpretación** | Baja actividad indica problemas socioeconómicos |
| **Fuente** | Registro de Actividad Comercial del Ayuntamiento |
| **Significado** | Vitalidad económica y oportunidades de empleo |
| **Problemas captados** | Declive económico, desempleo, falta de servicios |

### 📈 Fórmula del Índice

```
ÍNDICE DE PRIORIDAD = 
    0.30 × Normalizar(Quejas) +
    0.20 × Normalizar(Contaminación) +
    0.15 × Normalizar(Ruido) +
    0.15 × Normalizar(ÉficitVerde) +
    0.10 × Normalizar(Equipamientos) +
    0.10 × Normalizar(Comercios)

Resultado: Escala 0-100
- 0-40:   Zona en buen estado
- 40-60:  Requiere seguimiento
- 60-80:  Intervención recomendada
- 80-100: Intervención urgente/crítica
```

### 🎯 ¿Qué se considera "Problemático"?

Se consideran problemáticas aquellas zonas que presentan:

| Problema | Indicador | Umbral |
|----------|-----------|--------|
| **Ciudadanos descontentos** | Quejas altas | >250/período |
| **Aire contaminado** | Contaminación | >60 índice |
| **Ruido excesivo** | Acústica | >72 dB |
| **Falta de naturaleza** | Zonas verdes | Índice alto |
| **Servicios insuficientes** | Equipamientos | Baja disponibilidad |
| **Declive económico** | Comercios | <150 activos |

---

## 📊 Indicadores en la Plataforma

| Indicador | Peso | Fuente | Problema |
|-----------|------|--------|---------|
| Quejas ciudadanas | 30% | Portal Datos Abiertos | Insatisfacción ciudadana |
| Contaminación del aire | 20% | Red Monitoreo Ambiental | Salud respiratoria |
| Ruido | 15% | Red Monitoreo Acústico | Calidad de vida |
| Zonas verdes | 15% | Espacios Públicos | Ocio y clima urbano |
| Servicios públicos | 10% | Catálogo Municipal | Acceso a servicios |
| Actividad comercial | 10% | Registro Comercial | Vitalidad económica |

---

## 🗂️ Estructura del Proyecto

```
fuenlabrada-smart-priorities/
│
├── app.py                           # Aplicación principal Streamlit
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
│
├── src/                             # Módulos de lógica
│   ├── __init__.py
│   ├── data_loader.py              # Carga desde API CKAN y archivos
│   ├── cleaning.py                 # Limpieza y normalización de datos
│   ├── indicators.py               # Cálculo del índice de prioridad
│   ├── model.py                    # Modelo predictivo (Random Forest)
│   ├── maps.py                     # Visualización en mapas
│   └── recommendations.py          # Motor de recomendaciones
│
├── data/                            # Datos (ignorado en repositorio)
│   ├── raw/                        # Datos descargados de la API
│   └── processed/                  # Datos procesados
│
└── notebooks/                       # Análisis exploratorio
    └── exploracion.ipynb           # Notebook con EDA
```

---

## ⚙️ Instalación

### Requisitos Previos
- Python 3.9+
- pip o conda

### Pasos de Instalación

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Uso

### Ejecutar la Aplicación

#### Windows:
```bash
streamlit run app.py
```

#### macOS/Linux:
```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### Carga de Datos

La aplicación soporta dos modos:

1. **Datos de Demostración** (Recomendado para empezar)
   - Datos sintéticos pero realistas
   - Modelo pre-entrenado
   - Análisis completo

2. **Datos Propios**
   - Cargar CSV o XLSX
   - Auto-detección de columnas
   - Integración con datos públicos
   - Entrenamiento automático del modelo

---

## 📦 Dependencias Principales

```
streamlit>=1.28.0          # Framework web
pandas>=2.1.0              # Análisis de datos
numpy>=1.26.0              # Computación numérica
plotly>=5.17.0             # Visualizaciones interactivas
scikit-learn>=1.4.0        # Machine Learning
folium>=0.14.0             # Mapas Leaflet
pydeck>=0.8.0              # Mapas Mapbox
geopandas>=0.14.0          # Datos geoespaciales
requests>=2.31.0           # Conexión API
openpyxl>=3.1.0            # Lectura de Excel
```

---

## 🔄 Metodología

### 1. **Carga de Datos**
- Origen principal: **Portal de Datos Abiertos de Fuenlabrada** (https://datosabiertos.ayto-fuenlabrada.es/)
- Formato: CSV/XLSX desde CKAN
- Cobertura: Todas las zonas de Fuenlabrada
- Actualización: Trimestral
- Licencia: CC0 1.0 (Dominio público)
- Seguridad: Datos públicos, sin información sensible

### 2. **Limpieza y Preparación**
- Normalización de columnas (lowercase, sin espacios)
- Detección automática de tipos de datos
- Manejo de valores faltantes (estrategia mediana)
- Eliminación de duplicados
- Validación de rangos (ej: ruido 0-120 dB)

### 3. **Cálculo del Índice de Prioridad**
El índice combina 6 indicadores en una métrica única 0-100:

```
Índice = 0.30×Quejas + 0.20×Contaminación + 0.15×Ruido + 
         0.15×ÉficitVerde + 0.10×Equipamientos + 0.10×Comercios

Pasos:
1. Normalizar cada indicador a escala 0-100
2. Aplicar pesos según importancia municipal
3. Sumar componentes ponderadas
4. Resultado: Escala 0-100
5. Clasificar en nivel: Baja/Media/Alta/Crítica
```

### 4. **Análisis por Ejes de Sostenibilidad**
- **👥 Eje Social** (Quejas + Servicios): Satisfacción ciudadana y acceso a servicios
- **🌳 Eje Ambiental** (Contaminación + Ruido + Verdes): Sostenibilidad y calidad ambiental
- **💰 Eje Económico** (Comercios): Vitalidad económica y oportunidades de empleo

### 5. **Predicción con Machine Learning**
El modelo de predicción aprende de los 6 indicadores para anticipar problemas futuros:

**Algoritmo:** Random Forest Regressor
- 100 árboles de decisión independientes
- Cada árbol aprende relaciones entre indicadores
- La predicción es el promedio de todos los árboles

**Entrada:** Mediciones actuales de 6 indicadores por zona
**Salida:** Pronóstico del Índice de Prioridad (próxima evaluación)
**Validación:** Cross-validation 5-fold con métricas RMSE y R²

**¿Cómo funciona?**
1. Lee los valores actuales de cada indicador
2. Identifica patrones históricos (tendencias)
3. Predice si cada indicador mejorará o empeorará
4. Calcula el índice futuro esperado
5. Genera alertas de riesgo

**Interpretación de resultados:**
- 🔴 Riesgo Alto (Índice futuro > 80): Intervención urgente
- 🟠 Riesgo Medio (60-80): Monitoreo activo
- 🟡 Riesgo Bajo (40-60): Seguimiento
- 🟢 Sin riesgo (<40): Mantener

### 6. **Recomendaciones Automáticas**
- Reglas basadas en indicadores (ej: si ruido > 75dB → "Controlar focos sonoros")
- Priorización según nivel de criticidad
- Enfoque específico por zona y eje
- Acciones accionables y basadas en datos

### 7. **Trazabilidad de Datos**
- Origen documentado para cada valor
- Fechas de actualización de fuentes
- Validación de integridad
- Reportes de calidad de datos

---

## 📈 Resultados Esperados

### Para el Ayuntamiento
- **Visión clara** de dónde actuar primero
- **Priorización objetiva** basada en datos
- **Recomendaciones accionables** por zona
- **Alertas de tendencias** futuras

### Para el Proyecto Hackathon
- ✅ Uso de datos públicos abiertos
- ✅ Análisis multidimensional
- ✅ Predicción con ML
- ✅ Interfaz web profesional
- ✅ Documentación completa
- ✅ Aplicación práctica en contexto real

---

## 📊 Ejemplo de Salida

### Zona: Centro (Índice: 84/100 - CRÍTICA)

**Desglose de Prioridad:**
- Quejas: 25 pts (84% * 30%)
- Contaminación: 16 pts (80% * 20%)
- Ruido: 12 pts (80% * 15%)
- Zonas verdes: 10 pts (67% * 15%)
- Servicios: 8 pts (80% * 10%)
- Comercio: 8 pts (80% * 10%)

**Recomendaciones:**
1. Reforzar atención ciudadana (muchas quejas)
2. Controlar focos de contaminación
3. Aumentar sombra urbana
4. Mejorar servicios públicos
5. Impulsar actividad comercial

**Predicción Futuro:**
- Prioridad estimada: 89/100 (Empeora)
- Riesgo: Alto
- Tendencia: -5 puntos (negativa)

---

## 🔬 Limitaciones y Mejoras Futuras

### Limitaciones Actuales
- Datos de demostración (no reales)
- Modelo sin histórico de datos (menos precisión)
- Algunas variables faltantes según disponibilidad de datos públicos
- Mapa de demostración (sin coordenadas reales)

### Mejoras Futuras
- Integración con API en tiempo real
- Histórico de datos (predicciones más precisas)
- Más indicadores (transporte, educación, salud)
- Análisis de series temporales
- Dashboard de evolución histórica
- Alertas automáticas por email
- Exportación de reportes PDF
- Integración con herramientas municipales

---

## 👨‍💻 Arquitectura Técnica

### Backend
- **Python 3.9+**
- **pandas**: Procesamiento de datos
- **scikit-learn**: Machine Learning
- **numpy**: Computación numérica

### Frontend
- **Streamlit**: Interfaz web interactiva
- **Plotly**: Gráficos interactivos
- **Folium**: Mapas interactivos

### Datos
- **API CKAN**: Fuenlabrada Open Data
- **CSV/XLSX**: Carga local

---

## 📝 Notas de Desarrollo

### Variables de Entrada Requeridas

El DataFrame debe contener al menos:
```python
df = pd.DataFrame({
    'zona': str,                          # Nombre de la zona
    'quejas': float,                      # Número de quejas
    'contaminacion': float,               # Índice de contaminación (0-100)
    'ruido': float,                       # Decibilios o índice (0-100)
    'zonas_verdes': float,               # Área en m² o índice (0-100)
    'servicios_publicos': float,         # Número o índice (0-100)
    'actividad_comercial': float,        # Número de negocios o índice (0-100)
    # Opcionales para mapa:
    'latitud': float,                     # Coordenada Y
    'longitud': float,                    # Coordenada X
})
```

### Ejecución en Línea de Comandos

```bash
# Desarrollo
streamlit run app.py

# Producción
streamlit run app.py --logger.level=warning

# Con puerto específico
streamlit run app.py --server.port 8080
```

---

## 📞 Soporte y Contacto

**Proyecto:** DATA-HACK-FUENLABRADA 2026
**Formato:** Análisis de Datos Abiertos
**Tecnologías:** Python, Streamlit, Machine Learning

---

## 📄 Licencia

Proyecto abierto para uso educativo y municipal. Los datos utilizados son de origen público (Portal de Datos Abiertos de Fuenlabrada).

---

**Última actualización:** Mayo 2026
**Versión:** 1.0 - Versión inicial para Hackathon

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
