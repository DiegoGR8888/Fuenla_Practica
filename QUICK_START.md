# 🚀 Guía Rápida de Inicio

## ⚡ En 3 pasos: Levanta la aplicación

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar la app
```bash
streamlit run app.py
```

### Paso 3: Abre en navegador
Se abrirá automáticamente en `http://localhost:8501`

---

## 🎮 Primera vez usando la app

1. **Selecciona "Datos de demostración"** en el sidebar izquierdo (👈 Lado izquierdo)
2. **Espera 3-5 segundos** a que se carguen los datos
3. **Navega por las 7 pestañas** para ver el análisis completo:

| Pestaña | Descripción |
|---------|------------|
| 🏙️ **Inicio** | Resumen ejecutivo con métricas principales |
| 📍 **Mapa** | Mapa interactivo de Fuenlabrada con zonas coloreadas |
| ⭐ **Índice** | Ranking de zonas ordenadas por prioridad (0-100) |
| 🌳 **Ambiente** | Análisis de contaminación, ruido y zonas verdes |
| 🤖 **Predicción** | Modelo ML que predice prioridades futuras |
| 🧠 **Recomendaciones** | Acciones sugeridas automáticamente por zona |
| 📦 **Datos** | Descarga resultados, ve estructura de datos |

---

## 📥 Cargar tus propios datos

### Paso 1: Prepara tu archivo
Crea un archivo CSV o XLSX con tus datos

### Paso 2: En la app
1. En el sidebar, selecciona **"📂 Cargar CSV/XLSX"**
2. Haz clic en **"Selecciona CSV o XLSX"**
3. Elige tu archivo

### Paso 3: Auto-procesamiento
✨ **La app automáticamente:**
- Detecta columnas de zona, coordenadas, etc.
- Limpia datos
- Calcula el índice de prioridad
- Entrena el modelo ML
- Genera recomendaciones

---

## 📊 Formato de Datos

### Mínimo requerido (6 columnas):

```csv
zona,quejas,contaminacion,ruido,zonas_verdes,servicios_publicos,actividad_comercial
Centro,342,85.5,78.2,12.3,8,156
El Naranjo,245,70.2,65.1,25.1,6,95
Loranca,180,60.0,55.5,30.2,5,110
```

### Recomendado (8+ columnas):

```csv
zona,quejas,contaminacion,ruido,zonas_verdes,servicios_publicos,actividad_comercial,latitud,longitud,poblacion
Centro,342,85.5,78.2,12.3,8,156,40.3215,-3.8065,15000
El Naranjo,245,70.2,65.1,25.1,6,95,40.3250,-3.8020,12000
```

---

## 📋 Descripción de Columnas

| Columna | Tipo | Rango | Descripción |
|---------|------|-------|------------|
| `zona` | String | - | Nombre del barrio/zona |
| `quejas` | Número | 0-1000 | Número de quejas ciudadanas |
| `contaminacion` | Número | 0-200 | Índice de contaminación (µg/m³) |
| `ruido` | Número | 40-90 | Nivel de ruido (decibelios) |
| `zonas_verdes` | Número | 0-100 | Área o índice de espacios verdes |
| `servicios_publicos` | Número | 0-50 | Número de equipamientos públicos |
| `actividad_comercial` | Número | 0-500 | Número de negocios/empleos |
| `latitud` | Número | 40.30-40.35 | Coordenada Y (opcional) |
| `longitud` | Número | -3.85 a -3.75 | Coordenada X (opcional) |
| `poblacion` | Número | - | Población de la zona (opcional) |

---

## 🎯 ¿Qué ve en cada pestaña?

### 🏙️ Inicio
- Total de zonas analizadas
- Índice promedio
- Número de zonas críticas
- Gráfico de distribución por prioridad
- Impactos por eje (social, ambiental, económico)

### 📍 Mapa
- Visualización geográfica de Fuenlabrada
- Zoom interactivo
- Colores según prioridad:
  - 🟢 Verde: Baja (0-40)
  - 🟡 Amarillo: Media (40-60)
  - 🟠 Naranja: Alta (60-80)
  - 🔴 Rojo: Crítica (80-100)
- Popup con información de cada zona

### ⭐ Índice Urbano
- Ranking Top 15 de zonas
- Tabla con índices exactos
- Estadísticas (máximo, mínimo, mediana)
- Explicación de la fórmula

### 🌳 Medio Ambiente
- Top 10 zonas con mayor contaminación
- Top 10 zonas con mayor ruido
- Top 10 zonas con déficit de zonas verdes
- Recomendaciones por zona ambiental

### 🤖 Predicción
- Métricas del modelo (MAE, R², MSE)
- Importancia de cada indicador
- Predicción vs Actual (Top 10 zonas)
- Tabla con predicciones detalladas
- Detección de tendencias (mejora/empeora)

### 🧠 Recomendaciones
- Top 5 acciones municipales
- Zonas prioritarias por eje
- Recomendaciones personalizadas por zona
- Acciones específicas según problema

### 📦 Datos
- Datasets cargados (estructura)
- Reporte de calidad de datos
- DataFrame maestro completo
- **Botón para descargar CSV** con todos los resultados

---

## 🐛 Solucionar Problemas

### Error: "Module not found"
```bash
# Asegúrate de estar en el directorio correcto
cd Fuenla_Practica

# Activa el entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "Port 8501 already in use"
```bash
# Usa otro puerto
streamlit run app.py --server.port 8502
```

### El archivo no carga / Error con formato
- ✅ Asegúrate que es CSV o XLSX
- ✅ Verifica que las columnas están en minúsculas
- ✅ Prueba primero con los datos de demostración
- ✅ Sin caracteres especiales excepto guion bajo (_)

### Datos de demostración se ven extraños
- Haz clic en la pestaña "Datos" → "Reporte de Calidad"
- Verifica que los datos tengan sentido
- Prueba con tus propios datos

---

## 💡 Tips Útiles

1. **Datos Faltantes**: Si un CSV tiene valores vacíos, la app los completa automáticamente (con mediana)

2. **Nombres de Columnas**: Puede usar:
   - `zona`, `barrio`, `distrito`, `localidad` (cualquiera funciona)
   - `quejas`, `incidencias`, `denuncias`
   - `contaminacion`, `pm10`, `calidad_aire`
   - `ruido`, `decibelios`, `db`
   - `verde`, `parques`, `arbolado`

3. **Rendimiento**: Con +100 zonas puede tardar +10 segundos

4. **Reutilizar Resultados**: Descarga el CSV desde "Datos" y úsalo en el siguiente análisis

5. **Modelo ML**: Mejora automáticamente al tener más datos históricos

---

## 📖 Documentación Completa

- **README.md** → Descripción técnica completa
- **DEVELOPMENT.md** → Guía de desarrollo
- **IMPLEMENTATION_NOTES.md** → Notas técnicas detalladas

---

## ✅ Checklist Rápido

- [ ] Python 3.9+ instalado (`python --version`)
- [ ] Estás en la carpeta `Fuenla_Practica`
- [ ] Ejecutaste `pip install -r requirements.txt`
- [ ] Ejecutaste `streamlit run app.py`
- [ ] Se abrió http://localhost:8501 en el navegador
- [ ] Seleccionaste "Datos de demostración"
- [ ] Ves el dashboard con 7 pestañas
- [ ] ¡Celebra! 🎉

---

**¡Disfruta analizando!** 📊🏛️📍

**Hackathon Fuenlabrada 2026** - Datos Abiertos para Decisiones Inteligentes
Centro,342,85.5,78.2,12.3,8,156,40.3210,-3.8045
```

---

## Troubleshooting rápido

| Problema | Solución |
|----------|----------|
| "ModuleNotFoundError" | Ejecuta: `pip install -r requirements.txt` |
| Puerto 8501 en uso | Ejecuta: `streamlit run app.py --server.port 8080` |
| Datos no cargados | Recarga la página (F5) |
| Mapa no aparece | Asegúrate de tener "latitud" y "longitud" en tu CSV |

---

## Entender el Índice de Prioridad

**Fórmula:**
```
Índice = (30% Quejas + 20% Contaminación + 15% Ruido + 
          15% Zonas Verdes + 10% Servicios + 10% Comercio)
```

**Clasificación:**
- 🟢 **0-40**: Baja prioridad
- 🟡 **40-60**: Media prioridad
- 🟠 **60-80**: Alta prioridad
- 🔴 **80-100**: Crítica (acción urgente)

---

## Características principales

✅ **Mapa interactivo** - Visualiza zonas por color de prioridad
✅ **Índice inteligente** - Combina 6 indicadores en 1 puntuación
✅ **Análisis ambiental** - Contaminación, ruido, zonas verdes
✅ **Predicción ML** - Random Forest predice problemas futuros
✅ **Recomendaciones** - Acciones automáticas por zona
✅ **Dashboard completo** - Gráficos y estadísticas
✅ **Descarga de datos** - Exporta resultados a CSV

---

## Preguntas frecuentes

**¿Necesito datos en un formato específico?**
No, la app detecta automáticamente zonas, coordenadas y números. Solo asegúrate de que la primera fila tenga nombres de columnas.

**¿Cuántos datos necesito?**
Mínimo 5 zonas. Con 10+ obtienes un modelo más fiable.

**¿El modelo ML es preciso?**
Es un prototipo que mejora con más datos históricos. Úsalo como indicador, no como predicción absoluta.

**¿Puedo usar datos de otro municipio?**
Sí, la app funciona con cualquier estructura de zonas + indicadores.

**¿Dónde guarda los datos?**
Todo se procesa localmente. Los datos subidos se usan solo en sesión.

---

## Estructura de carpetas

```
fuenlabrada-smart-priorities/
├── app.py                 ← AQUÍ ESTÁ LA MAGIA ✨
├── requirements.txt       ← Dependencias
├── README.md              ← Documentación completa
├── src/
│   ├── data_loader.py     ← Carga datos
│   ├── cleaning.py        ← Limpia datos
│   ├── indicators.py      ← Calcula índices
│   ├── maps.py            ← Mapas
│   ├── model.py           ← ML
│   └── recommendations.py ← Recomendaciones
├── data/
│   ├── raw/               ← Tus CSVs aquí
│   └── processed/         ← Datos procesados
└── .streamlit/
    └── config.toml        ← Configuración Streamlit
```

---

## Tips profesionales

1. **Normaliza tus datos**: Si tus indicadores tienen escalas muy diferentes, la app los normalizará automáticamente.

2. **Usa coordenadas**: Con latitud/longitud obtendrás mapas bonitos. Sin ellas, funciona igualmente pero sin visualización geográfica.

3. **Prueba los sliders**: En futuras versiones podrás ajustar los pesos del índice interactivamente.

4. **Descarga los resultados**: Usa el CSV exportado en otras herramientas de BI.

5. **Comparte con stakeholders**: Los mapas y gráficos son muy efectivos para presentaciones.

---

## Contacto y soporte

Para dudas: data-hack-fuenlabrada2026@ayto-fuenlabrada.es

¡Que disfrutes explorando los datos de Fuenlabrada! 🚀
