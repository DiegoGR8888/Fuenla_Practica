"""
ML Model Module
Modelo predictivo para prioridad futura
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from typing import Tuple, Optional, Dict
import streamlit as st


class PriorityPredictor:
    """
    Modelo de predicción de prioridad urbana futura
    """
    
    def __init__(self, random_state: int = 42):
        """
        Inicializa el predictor
        
        Args:
            random_state: Seed para reproducibilidad
        """
        self.model = None
        self.scaler = StandardScaler()
        self.feature_cols = None
        self.is_trained = False
        self.random_state = random_state
        self.metrics = {}
    
    def prepare_features(self, df: pd.DataFrame) -> Optional[np.ndarray]:
        """
        Prepara características para el modelo
        
        Args:
            df: DataFrame con datos normalizados
            
        Returns:
            np.ndarray: Matriz de características
        """
        
        # Selecciona columnas normalizadas disponibles
        feature_keywords = ["_norm"]
        available_features = [col for col in df.columns if feature_keywords[0] in col]
        
        if not available_features:
            # Si no hay columnas normalizadas, usa numéricas disponibles
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # Excluye columnas que ya no son features
            exclude = ["indice_prioridad", "prediccion_prioridad", "poblacion", "latitud", "longitud"]
            available_features = [col for col in numeric_cols if col not in exclude]
        
        if not available_features:
            return None
        
        self.feature_cols = available_features
        X = df[available_features].fillna(0).values
        return X
    
    def train(self, df: pd.DataFrame, target_col: str = "indice_prioridad", 
              test_size: float = 0.2) -> Dict:
        """
        Entrena el modelo predictivo
        
        Args:
            df: DataFrame con datos de entrenamiento
            target_col: Columna objetivo
            test_size: Proporción de test
            
        Returns:
            Dict: Métricas de entrenamiento
        """
        
        # Prepara features
        X = self.prepare_features(df)
        if X is None or len(X) < 2:
            return {"error": "No hay suficientes features para entrenar"}
        
        # Target
        y = df[target_col].fillna(0).values
        
        # Valida que hay datos
        if len(X) < 2:
            return {"error": "No hay suficientes datos para entrenar"}
        
        try:
            # Split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=self.random_state
            )
            
            # Escala datos
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Entrena modelo
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=3,
                min_samples_leaf=1,
                random_state=self.random_state,
                n_jobs=-1
            )
            self.model.fit(X_train_scaled, y_train)
            
            # Evalúa
            y_pred = self.model.predict(X_test_scaled)
            
            self.metrics = {
                "mse": mean_squared_error(y_test, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
                "mae": mean_absolute_error(y_test, y_pred),
                "r2": r2_score(y_test, y_pred),
                "train_size": len(X_train),
                "test_size": len(X_test),
                "n_features": X.shape[1],
            }
            
            self.is_trained = True
            return self.metrics
            
        except Exception as e:
            return {"error": str(e)}
    
    def predict(self, df: pd.DataFrame) -> Optional[np.ndarray]:
        """
        Realiza predicciones
        
        Args:
            df: DataFrame con datos para predecir
            
        Returns:
            np.ndarray: Predicciones
        """
        
        if not self.is_trained or self.model is None:
            return None
        
        X = self.prepare_features(df)
        if X is None:
            return None
        
        try:
            X_scaled = self.scaler.transform(X)
            predictions = self.model.predict(X_scaled)
            return predictions
        except Exception as e:
            print(f"Error en predicción: {str(e)}")
            return None
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Retorna importancia de features
        
        Returns:
            pd.DataFrame: Importancia de cada feature
        """
        
        if self.model is None or self.feature_cols is None:
            return pd.DataFrame()
        
        importance = self.model.feature_importances_
        feature_importance = pd.DataFrame({
            "feature": self.feature_cols,
            "importance": importance,
        }).sort_values("importance", ascending=False)
        
        return feature_importance
    
    def get_metrics_summary(self) -> str:
        """
        Retorna resumen de métricas en texto
        
        Returns:
            str: Resumen formateado
        """
        
        if not self.metrics:
            return "No hay métricas disponibles. Entrena el modelo primero."
        
        if "error" in self.metrics:
            return f"Error: {self.metrics['error']}"
        
        summary = f"""
**Métricas del Modelo Predictivo:**
- R² Score: {self.metrics['r2']:.3f}
- RMSE: {self.metrics['rmse']:.2f}
- MAE: {self.metrics['mae']:.2f}
- Datos de entrenamiento: {self.metrics['train_size']}
- Datos de prueba: {self.metrics['test_size']}
- Features utilizadas: {self.metrics['n_features']}

*El modelo predictivo es un prototipo que mejora automáticamente con más datos históricos.*
        """
        
        return summary


def calculate_trend(current: float, predicted: float) -> Tuple[str, str]:
    """
    Calcula tendencia entre valor actual y predicho
    
    Args:
        current: Valor actual del índice
        predicted: Valor predicho del índice
        
    Returns:
        Tuple: (tendencia, emoji)
    """
    
    diff = predicted - current
    
    if diff > 5:
        return "Empeora", "📈"
    elif diff > 1:
        return "Ligeramente empeora", "📊"
    elif diff < -5:
        return "Mejora", "📉"
    elif diff < -1:
        return "Ligeramente mejora", "📊"
    else:
        return "Estable", "➡️"


def get_risk_level(predicted_index: float) -> str:
    """
    Determina nivel de riesgo futuro
    
    Args:
        predicted_index: Índice predicho
        
    Returns:
        str: Nivel de riesgo
    """
    
    if predicted_index < 40:
        return "Bajo"
    elif predicted_index < 60:
        return "Medio"
    elif predicted_index < 80:
        return "Alto"
    else:
        return "Crítico"


def create_naive_forecast(df: pd.DataFrame, growth_rate: float = 0.02) -> np.ndarray:
    """
    Crea predicción ingenua (baseline) basada en tendencia
    
    Args:
        df: DataFrame con índices actuales
        growth_rate: Tasa de crecimiento estimada
        
    Returns:
        np.ndarray: Predicciones
    """
    
    current_index = df["indice_prioridad"].values
    predictions = current_index * (1 + growth_rate)
    
    # Limita a [0, 100]
    predictions = np.clip(predictions, 0, 100)
    
    return predictions


def ensemble_predictions(
    ml_predictions: np.ndarray,
    naive_predictions: np.ndarray,
    ml_weight: float = 0.7
) -> np.ndarray:
    """
    Combina predicciones de ML y naive en ensemble
    
    Args:
        ml_predictions: Predicciones del modelo ML
        naive_predictions: Predicciones naive
        ml_weight: Peso para predicciones ML [0, 1]
        
    Returns:
        np.ndarray: Predicciones ensemble
    """
    
    ensemble = (ml_predictions * ml_weight) + (naive_predictions * (1 - ml_weight))
    return np.clip(ensemble, 0, 100)


def add_predictions_to_df(
    df: pd.DataFrame,
    predictor: PriorityPredictor
) -> pd.DataFrame:
    """
    Añade predicciones al DataFrame
    
    Args:
        df: DataFrame original
        predictor: Modelo entrenado
        
    Returns:
        pd.DataFrame: Con predicciones añadidas
    """
    
    df = df.copy()
    
    # Obtiene predicciones ML
    ml_pred = predictor.predict(df)
    
    if ml_pred is not None:
        # Obtiene predicción naive
        naive_pred = create_naive_forecast(df, growth_rate=0.03)
        
        # Combina
        ensemble_pred = ensemble_predictions(ml_pred, naive_pred, ml_weight=0.6)
        
        df["prediccion_prioridad"] = ensemble_pred
    else:
        # Fallback a predicción naive
        df["prediccion_prioridad"] = create_naive_forecast(df, growth_rate=0.02)
    
    # Calcula tendencia
    df["tendencia"] = df.apply(
        lambda row: calculate_trend(
            row["indice_prioridad"],
            row["prediccion_prioridad"]
        )[0],
        axis=1
    )
    
    df["riesgo_futuro"] = df["prediccion_prioridad"].apply(get_risk_level)
    
    return df
