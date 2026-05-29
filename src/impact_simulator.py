"""
Impact Simulator Module
=======================
Simula actuaciones municipales, estima impacto ciudadano y genera recomendaciones
con reglas explicables + apoyo opcional de Ollama.
"""

from __future__ import annotations

import json
from typing import Dict, List, Tuple

import pandas as pd
import requests


WEIGHTS: Dict[str, float] = {
    "quejas": 0.30,
    "contaminacion": 0.20,
    "ruido": 0.15,
    "zonas_verdes": 0.15,
    "servicios": 0.10,
    "comercio": 0.10,
}

NORM_COLUMNS: Dict[str, str] = {
    "quejas": "quejas_norm",
    "contaminacion": "contaminacion_norm",
    "ruido": "ruido_norm",
    "zonas_verdes": "zonas_verdes_norm",
    "servicios": "servicios_norm",
    "comercio": "comercio_norm",
}

DISPLAY_NAMES: Dict[str, str] = {
    "quejas": "Quejas ciudadanas",
    "contaminacion": "Contaminación del aire",
    "ruido": "Ruido urbano",
    "zonas_verdes": "Déficit de zonas verdes",
    "servicios": "Falta de servicios públicos",
    "comercio": "Baja actividad comercial",
}

COST_FACTOR = {
    "Bajo": 1.0,
    "Bajo/Medio": 1.3,
    "Medio": 1.7,
    "Medio/Alto": 2.1,
    "Alto": 2.7,
}

IMPACT_FACTOR = {
    "Bajo": 1.0,
    "Medio": 1.4,
    "Medio/Alto": 1.7,
    "Alto": 2.0,
    "Muy alto": 2.4,
}

ACTION_CATALOG: List[Dict] = [
    {
        "accion": "Plan de respuesta rápida a incidencias vecinales",
        "eje": "Social",
        "indicador": "quejas",
        "coste": "Bajo/Medio",
        "impacto": "Alto",
        "plazo": "Corto plazo",
        "reducciones": {"quejas": 25},
        "descripcion": "Refuerzo de inspecciones, resolución de incidencias y canal directo con vecinos.",
    },
    {
        "accion": "Plan de reducción de contaminación urbana",
        "eje": "Ambiental",
        "indicador": "contaminacion",
        "coste": "Medio/Alto",
        "impacto": "Alto",
        "plazo": "Medio plazo",
        "reducciones": {"contaminacion": 20, "ruido": 5},
        "descripcion": "Medidas sobre tráfico, control de emisiones y mejora de movilidad sostenible.",
    },
    {
        "accion": "Reducir velocidad y pacificar calles",
        "eje": "Ambiental / Movilidad",
        "indicador": "ruido",
        "coste": "Bajo/Medio",
        "impacto": "Medio/Alto",
        "plazo": "Corto plazo",
        "reducciones": {"ruido": 22, "contaminacion": 8},
        "descripcion": "Zonas 30, calmado de tráfico, pasos elevados y reordenación de circulación.",
    },
    {
        "accion": "Crear microparques, sombra y corredores verdes",
        "eje": "Ambiental / Salud",
        "indicador": "zonas_verdes",
        "coste": "Medio",
        "impacto": "Muy alto",
        "plazo": "Medio plazo",
        "reducciones": {"zonas_verdes": 30, "contaminacion": 6, "ruido": 6},
        "descripcion": "Más arbolado, pequeñas zonas verdes y conexión peatonal saludable entre barrios.",
    },
    {
        "accion": "Ampliar cobertura de equipamientos públicos",
        "eje": "Social",
        "indicador": "servicios",
        "coste": "Alto",
        "impacto": "Muy alto",
        "plazo": "Largo plazo",
        "reducciones": {"servicios": 30, "quejas": 8},
        "descripcion": "Refuerzo de centros, horarios, accesibilidad y servicios municipales cercanos.",
    },
    {
        "accion": "Programa de impulso al comercio local",
        "eje": "Económico",
        "indicador": "comercio",
        "coste": "Medio",
        "impacto": "Medio/Alto",
        "plazo": "Medio plazo",
        "reducciones": {"comercio": 28, "quejas": 5},
        "descripcion": "Bonos comercio, campañas locales, apoyo a emprendedores y mejora del espacio urbano comercial.",
    },
]


def classify_priority_value(value: float) -> str:
    """Clasifica un índice 0-100 en Baja/Media/Alta/Crítica."""
    if value < 40:
        return "Baja"
    if value < 60:
        return "Media"
    if value < 80:
        return "Alta"
    return "Crítica"


def recalculate_priority_from_norms(row: pd.Series) -> float:
    """Recalcula el índice de prioridad usando las columnas *_norm disponibles."""
    total_weight = 0.0
    weighted_sum = 0.0

    for key, weight in WEIGHTS.items():
        col = NORM_COLUMNS[key]
        if col in row.index:
            value = float(pd.to_numeric(row[col], errors="coerce") or 0)
            weighted_sum += value * weight
            total_weight += weight

    if total_weight == 0:
        return 0.0
    return max(0.0, min(100.0, weighted_sum / total_weight))


def simulate_custom_intervention(row: pd.Series, reductions: Dict[str, float]) -> Tuple[pd.Series, Dict]:
    """
    Aplica reducciones porcentuales sobre indicadores normalizados.
    Una reducción en zonas_verdes_norm, servicios_norm o comercio_norm significa
    reducir el déficit, no reducir el recurso real.
    """
    simulated = row.copy()

    for key, reduction_pct in reductions.items():
        col = NORM_COLUMNS.get(key)
        if col in simulated.index:
            current = float(pd.to_numeric(simulated[col], errors="coerce") or 0)
            simulated[col] = max(0.0, current * (1 - reduction_pct / 100))

    current_index = float(row.get("indice_prioridad", recalculate_priority_from_norms(row)))
    new_index = recalculate_priority_from_norms(simulated)
    improvement = max(0.0, current_index - new_index)

    population = get_population(row)
    people_currently_affected = int(round(population * current_index / 100)) if population else 0
    people_benefited = int(round(population * improvement / 100)) if population else 0

    result = {
        "indice_actual": round(current_index, 2),
        "indice_simulado": round(new_index, 2),
        "mejora_puntos": round(improvement, 2),
        "prioridad_actual": str(row.get("prioridad", classify_priority_value(current_index))),
        "prioridad_simulada": classify_priority_value(new_index),
        "poblacion": population,
        "personas_afectadas_estimadas": people_currently_affected,
        "personas_beneficiadas_estimadas": people_benefited,
    }
    return simulated, result


def get_population(row: pd.Series) -> int:
    """Busca una columna de población de forma flexible."""
    for col in ["poblacion_2024", "poblacion", "habitantes", "residentes"]:
        if col in row.index:
            value = pd.to_numeric(row[col], errors="coerce")
            if pd.notna(value):
                return int(value)
    return 0


def explain_main_factors(row: pd.Series, top_n: int = 3) -> List[Dict]:
    """Devuelve los factores que más explican la prioridad de la zona."""
    factors = []
    for key, col in NORM_COLUMNS.items():
        if col in row.index:
            value = float(pd.to_numeric(row[col], errors="coerce") or 0)
            contribution = value * WEIGHTS[key]
            factors.append({
                "factor": DISPLAY_NAMES[key],
                "indicador": key,
                "valor_norm": round(value, 1),
                "contribucion": round(contribution, 1),
            })
    return sorted(factors, key=lambda x: x["contribucion"], reverse=True)[:top_n]


def rank_actions_for_zone(row: pd.Series, top_n: int = 6) -> pd.DataFrame:
    """Ordena actuaciones según gravedad, mejora simulada, población beneficiada y coste."""
    ranked = []

    for action in ACTION_CATALOG:
        indicator = action["indicador"]
        col = NORM_COLUMNS[indicator]
        severity = float(pd.to_numeric(row.get(col, 0), errors="coerce") or 0)

        _, sim_result = simulate_custom_intervention(row, action["reducciones"])
        improvement = sim_result["mejora_puntos"]
        benefited = sim_result["personas_beneficiadas_estimadas"]

        score = (
            severity * 0.45
            + improvement * 12
            + min(benefited / 1000, 25)
        ) * IMPACT_FACTOR[action["impacto"]] / COST_FACTOR[action["coste"]]

        if score >= 95:
            priority = "Muy alta"
        elif score >= 65:
            priority = "Alta"
        elif score >= 35:
            priority = "Media"
        else:
            priority = "Baja"

        ranked.append({
            "Acción": action["accion"],
            "Eje": action["eje"],
            "Coste estimado": action["coste"],
            "Impacto esperado": action["impacto"],
            "Plazo": action["plazo"],
            "Mejora estimada índice": round(improvement, 1),
            "Vecinos beneficiados estimados": benefited,
            "Prioridad acción": priority,
            "Puntuación": round(score, 1),
            "Descripción": action["descripcion"],
        })

    return pd.DataFrame(ranked).sort_values("Puntuación", ascending=False).head(top_n)


def ask_ollama_for_recommendation(
    zone_name: str,
    row: pd.Series,
    simulation_result: Dict,
    actions_df: pd.DataFrame,
    model: str = "llama3.2",
    host: str = "http://localhost:11434",
    timeout: int = 120,
) -> str:
    """
    Pide a Ollama una recomendación ejecutiva.
    Si Ollama no está activo, devuelve una explicación de fallback sin romper Streamlit.
    """
    factors = explain_main_factors(row, top_n=3)
    actions_payload = actions_df.drop(columns=["Puntuación"], errors="ignore").to_dict(orient="records")

    system_prompt = (
        "Eres un asesor técnico de un ayuntamiento. "
        "Responde en español, con tono claro, ejecutivo y orientado a impacto ciudadano. "
        "No inventes datos: usa solo los datos recibidos. "
        "Devuelve una recomendación accionable para presentar a responsables municipales."
    )

    user_prompt = f"""
Zona analizada: {zone_name}
Índice actual: {simulation_result['indice_actual']}
Índice simulado: {simulation_result['indice_simulado']}
Mejora estimada: {simulation_result['mejora_puntos']} puntos
Población estimada: {simulation_result['poblacion']}
Vecinos actualmente afectados estimados: {simulation_result['personas_afectadas_estimadas']}
Vecinos beneficiados estimados por el escenario: {simulation_result['personas_beneficiadas_estimadas']}
Factores principales: {json.dumps(factors, ensure_ascii=False)}
Ranking de acciones: {json.dumps(actions_payload, ensure_ascii=False)}

Redacta:
1. Diagnóstico breve.
2. Paquete de 3 acciones recomendado.
3. Justificación coste-impacto.
4. Frase final para vender impacto ciudadano.
"""

    try:
        response = requests.post(
            f"{host.rstrip('/')}/api/chat",
            json={
                "model": model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("message", {}).get("content", "").strip() or "Ollama respondió vacío."
    except Exception as exc:
        best_actions = actions_df.head(3)["Acción"].tolist() if not actions_df.empty else []
        return (
            "⚠️ **Ollama no está disponible ahora mismo**, así que se muestra una recomendación basada en reglas explicables.\n\n"
            f"**Diagnóstico:** la zona presenta un índice de prioridad de "
            f"{simulation_result['indice_actual']:.1f}, que podría bajar hasta "
            f"{simulation_result['indice_simulado']:.1f} con el escenario seleccionado.\n\n"
            f"**Acciones recomendadas:** {', '.join(best_actions) if best_actions else 'mantener seguimiento y priorizar según indicadores críticos'}.\n\n"
            f"**Impacto ciudadano estimado:** unas {simulation_result['personas_beneficiadas_estimadas']:,} personas podrían beneficiarse.\n\n"
            f"Detalle técnico: {exc}"
        )
