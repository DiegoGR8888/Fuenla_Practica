"""
Recommendations Module
Generación automática de recomendaciones
"""

import pandas as pd
from typing import Dict, List


class RecommendationEngine:
    """
    Motor de generación de recomendaciones
    """
    
    @staticmethod
    def get_zone_recommendation(row: pd.Series) -> str:
        """
        Genera recomendación para una zona
        
        Args:
            row: Serie con datos de una zona
            
        Returns:
            str: Recomendación generada
        """
        
        recommendations = []
        
        # Análisis de contaminación
        if "contaminacion_norm" in row.index:
            if row["contaminacion_norm"] > 70:
                recommendations.append(
                    "🌍 **Control ambiental**: Detectar y controlar focos de contaminación, "
                    "reducir presión ambiental del tráfico."
                )
            elif row["contaminacion_norm"] > 50:
                recommendations.append(
                    "🌍 **Monitoreo ambiental**: Aumentar seguimiento de contaminantes, "
                    "considerar restricciones de tráfico."
                )
        
        # Análisis de ruido
        if "ruido_norm" in row.index:
            if row["ruido_norm"] > 70:
                recommendations.append(
                    "🔊 **Control acústico**: Implementar barreras acústicas, reducir velocidades, "
                    "mejorar aislamiento de edificios sensibles."
                )
            elif row["ruido_norm"] > 50:
                recommendations.append(
                    "🔊 **Monitoreo acústico**: Establecer puntos de control, "
                    "regular horarios de obras."
                )
        
        # Análisis de zonas verdes
        if "zonas_verdes_norm" in row.index:
            if row["zonas_verdes_norm"] > 70:
                recommendations.append(
                    "🌳 **Actuación verde urgente**: Crear corredores verdes, microparques, "
                    "aumentar sombra urbana y superficies permeables."
                )
            elif row["zonas_verdes_norm"] > 50:
                recommendations.append(
                    "🌳 **Mejora verde**: Plantaciones estratégicas, mejora de parques existentes, "
                    "arbolado en calles."
                )
        
        # Análisis de quejas/incidencias
        if "quejas_norm" in row.index:
            if row["quejas_norm"] > 70:
                recommendations.append(
                    "👥 **Atención ciudadana urgente**: Reforzar canales de participación, "
                    "resolver incidencias prioritarias, mejorar comunicación."
                )
            elif row["quejas_norm"] > 50:
                recommendations.append(
                    "👥 **Mejora de servicios**: Establecer oficina de atención ciudadana local, "
                    "aumentar frecuencia de inspecciones."
                )
        
        # Análisis de servicios públicos
        if "servicios_norm" in row.index:
            if row["servicios_norm"] > 70:
                recommendations.append(
                    "🏥 **Ampliar servicios**: Crear o mejorar centros de salud, escuelas, "
                    "equipamientos públicos. Prioridad en cobertura básica."
                )
            elif row["servicios_norm"] > 50:
                recommendations.append(
                    "🏥 **Refuerzo de servicios**: Ampliar horarios, mejorar accesibilidad, "
                    "crear servicios complementarios."
                )
        
        # Análisis de actividad comercial
        if "comercio_norm" in row.index:
            if row["comercio_norm"] > 70:
                recommendations.append(
                    "🏪 **Revitalización económica**: Impulsar comercio local, apoyar emprendimiento, "
                    "mejorar imagen urbana para atraer inversión."
                )
            elif row["comercio_norm"] > 50:
                recommendations.append(
                    "🏪 **Dinamización económica**: Subvenciones a pequeños comercios, "
                    "mejorar accesibilidad y estacionamiento."
                )
        
        # Si no hay recomendaciones específicas
        if not recommendations:
            priority = row.get("prioridad", "Media")
            if priority == "Crítica":
                recommendations.append("⚠️ Requiere intervención integral urgente.")
            elif priority == "Alta":
                recommendations.append("🔔 Requiere actuación prioritaria en próximos meses.")
            else:
                recommendations.append("✅ Mantener monitoreo regular.")
        
        return "\n".join(recommendations)
    
    @staticmethod
    def get_top_actions(df: pd.DataFrame, top_n: int = 5) -> List[str]:
        """
        Genera lista de top acciones municipales recomendadas
        
        Args:
            df: DataFrame con análisis por zona
            top_n: Número de acciones a retornar
            
        Returns:
            List[str]: Lista de acciones ordenadas por impacto
        """
        
        actions = []
        
        # Análisis agregado
        critical_zones = len(df[df["prioridad"] == "Crítica"])
        high_zones = len(df[df["prioridad"] == "Alta"])
        
        avg_contam = df["contaminacion_norm"].mean() if "contaminacion_norm" in df.columns else 0
        avg_ruido = df["ruido_norm"].mean() if "ruido_norm" in df.columns else 0
        avg_verdes = df["zonas_verdes_norm"].mean() if "zonas_verdes_norm" in df.columns else 0
        avg_servicios = df["servicios_norm"].mean() if "servicios_norm" in df.columns else 0
        avg_comercio = df["comercio_norm"].mean() if "comercio_norm" in df.columns else 0
        
        # Ranking de acciones por impacto
        action_scores = {}
        
        if critical_zones > 0:
            action_scores["1. Crear plan de intervención urgente en zonas críticas"] = critical_zones * 10
        
        if avg_contam > 65:
            action_scores["2. Plan de reducción de contaminación urbana"] = avg_contam * 2
        
        if avg_verdes > 65:
            action_scores["3. Crear corredores verdes y microparques"] = avg_verdes * 1.8
        
        if avg_ruido > 65:
            action_scores["4. Implementar control acústico en puntos críticos"] = avg_ruido * 1.6
        
        if avg_servicios > 65:
            action_scores["5. Ampliar cobertura de servicios públicos"] = avg_servicios * 1.5
        
        if avg_comercio > 65:
            action_scores["6. Programa de impulso al comercio local"] = avg_comercio * 1.4
        
        if critical_zones + high_zones > len(df) * 0.3:
            action_scores["7. Mejorar canales de atención y participación ciudadana"] = (critical_zones + high_zones) * 1.2
        
        # Ordena por impacto
        sorted_actions = sorted(
            action_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Retorna top N
        return [action[0] for action in sorted_actions[:top_n]]
    
    @staticmethod
    def get_priority_summary(df: pd.DataFrame) -> Dict:
        """
        Resumen ejecutivo del análisis
        
        Args:
            df: DataFrame analizado
            
        Returns:
            Dict: Resumen con estadísticas
        """
        
        summary = {
            "total_zonas": len(df),
            "zonas_criticas": len(df[df["prioridad"] == "Crítica"]),
            "zonas_altas": len(df[df["prioridad"] == "Alta"]),
            "zonas_medias": len(df[df["prioridad"] == "Media"]),
            "zonas_bajas": len(df[df["prioridad"] == "Baja"]),
            "indice_promedio": df["indice_prioridad"].mean() if "indice_prioridad" in df.columns else 0,
            "peor_zona": df.loc[df["indice_prioridad"].idxmax()]["zona"] if "zona" in df.columns and "indice_prioridad" in df.columns else "?",
            "mejor_zona": df.loc[df["indice_prioridad"].idxmin()]["zona"] if "zona" in df.columns and "indice_prioridad" in df.columns else "?",
        }
        
        return summary
    
    @staticmethod
    def get_environmental_focus_areas(df: pd.DataFrame) -> List[str]:
        """
        Identifica zonas con mayor necesidad de intervención ambiental
        
        Args:
            df: DataFrame
            
        Returns:
            List[str]: Zonas priorizadas ambientalmente
        """
        
        if "impacto_ambiental" not in df.columns:
            return []
        
        top_env = df.nlargest(3, "impacto_ambiental")
        return top_env["zona"].tolist() if "zona" in df.columns else []
    
    @staticmethod
    def get_social_focus_areas(df: pd.DataFrame) -> List[str]:
        """
        Identifica zonas con mayor necesidad de intervención social
        
        Args:
            df: DataFrame
            
        Returns:
            List[str]: Zonas priorizadas socialmente
        """
        
        if "impacto_social" not in df.columns:
            return []
        
        top_social = df.nlargest(3, "impacto_social")
        return top_social["zona"].tolist() if "zona" in df.columns else []
    
    @staticmethod
    def get_economic_focus_areas(df: pd.DataFrame) -> List[str]:
        """
        Identifica zonas con mayor necesidad de intervención económica
        
        Args:
            df: DataFrame
            
        Returns:
            List[str]: Zonas priorizadas económicamente
        """
        
        if "impacto_economico" not in df.columns:
            return []
        
        top_econ = df.nlargest(3, "impacto_economico")
        return top_econ["zona"].tolist() if "zona" in df.columns else []
    
    @staticmethod
    def generate_comparative_analysis(df: pd.DataFrame, zone1: str, zone2: str) -> Dict:
        """
        Genera análisis comparativo entre dos zonas
        
        Args:
            df: DataFrame
            zone1: Primera zona a comparar
            zone2: Segunda zona a comparar
            
        Returns:
            Dict: Comparativa detallada
        """
        
        data1 = df[df["zona"] == zone1].iloc[0] if "zona" in df.columns and zone1 in df["zona"].values else None
        data2 = df[df["zona"] == zone2].iloc[0] if "zona" in df.columns and zone2 in df["zona"].values else None
        
        if data1 is None or data2 is None:
            return {"error": "Zona no encontrada"}
        
        comparison = {
            "zona1": zone1,
            "zona2": zone2,
            "indice_diferencia": data1["indice_prioridad"] - data2["indice_prioridad"],
            "prioritaria": zone1 if data1["indice_prioridad"] > data2["indice_prioridad"] else zone2,
        }
        
        # Componentes
        components = ["quejas_norm", "contaminacion_norm", "ruido_norm", 
                     "zonas_verdes_norm", "servicios_norm", "comercio_norm"]
        
        for comp in components:
            if comp in data1.index and comp in data2.index:
                comparison[f"{comp}_z1"] = data1[comp]
                comparison[f"{comp}_z2"] = data2[comp]
        
        return comparison
