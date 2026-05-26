# 🚀 Guía Rápida de Inicio

## En 3 pasos: Levanta la aplicación

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

## Primera vez usando la app

1. **Selecciona "Datos de demostración"** en el sidebar izquierdo
2. **Espera 5 segundos** a que se carguen los datos
3. **Navega por las pestañas** para ver el análisis:
   - 🏙️ **Inicio**: Resumen general
   - 📍 **Mapa**: Visualización geográfica
   - ⭐ **Índice**: Ranking de zonas
   - 🌳 **Ambiente**: Análisis ambiental
   - 🤖 **Predicción**: Modelo ML
   - 🧠 **Recomendaciones**: Acciones sugeridas
   - 📦 **Datos**: Descargar resultados

---

## Cargar tus propios datos

1. En el sidebar, selecciona **"Cargar CSV/XLSX"**
2. Haz clic en **"Selecciona CSV o XLSX"**
3. Elige tu archivo
4. ¡La app auto-detectará columnas de zona, coordenadas, etc.!

### Formato esperado (mínimo):
```
zona,quejas,contaminacion,ruido,zonas_verdes,servicios_publicos,actividad_comercial
Centro,342,85.5,78.2,12.3,8,156
```

### Formato completo (recomendado):
```
zona,quejas,contaminacion,ruido,zonas_verdes,servicios_publicos,actividad_comercial,latitud,longitud
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
