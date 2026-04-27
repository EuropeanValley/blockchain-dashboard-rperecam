"""
Script de entrenamiento offline para el modelo predictivo de dificultad de Bitcoin.
Este script ingesta datos históricos, realiza feature engineering, entrena un
Random Forest Regressor y exporta el modelo y las métricas para su uso en producción.
"""

import os
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

# --- 1. CONFIGURACIÓN DE RUTAS ---
# Obtenemos la ruta absoluta de la carpeta 'model' donde está este script
MODEL_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(MODEL_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "difficulty.json")

# Rutas de salida
MODEL_OUTPUT = os.path.join(MODEL_DIR, "rf_model.joblib")
METRICS_OUTPUT = os.path.join(MODEL_DIR, "metrics.json")
BACKTEST_OUTPUT = os.path.join(MODEL_DIR, "backtest_data.json")


def load_data() -> pd.DataFrame:
    """Carga y une los datos JSON."""
    print(" Cargando datos desde data/difficulty.json...")
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df_diff = pd.DataFrame(data.get("difficulty", []))
    df_diff = df_diff.rename(columns={"x": "timestamp", "y": "difficulty"})

    df_price = pd.DataFrame(data.get("market-price", []))
    df_price = df_price.rename(columns={"x": "timestamp", "y": "price"})

    df = pd.merge(df_diff, df_price, on="timestamp", how="inner")
    df['timestamp'] = df['timestamp'] / 1000
    df['date'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.sort_values('date').reset_index(drop=True)
    return df


def create_features(df: pd.DataFrame):
    """Genera las variables predictivas y el target (variación porcentual)."""
    print(" Aplicando Feature Engineering...")
    df['prev_diff'] = df['difficulty'].shift(1)
    df['diff_change_pct'] = (df['difficulty'] - df['prev_diff']) / df['prev_diff']

    df['prev_price'] = df['price'].shift(1)
    df['price_change_pct'] = (df['price'] - df['prev_price']) / df['prev_price']

    # Target: Predecimos el % de cambio del próximo ajuste
    df['target_next_diff_pct'] = df['diff_change_pct'].shift(-1)

    return df


def train_and_evaluate():
    """Flujo principal de entrenamiento y exportación."""
    df_raw = load_data()
    df_features = create_features(df_raw)

    # Separamos el último registro (el presente) para no usarlo en el entrenamiento
    df_train_ready = df_features.dropna().copy()

    # Definir variables
    features = ['difficulty', 'price', 'diff_change_pct', 'price_change_pct']
    X = df_train_ready[features]
    y = df_train_ready['target_next_diff_pct']

    # Split Cronológico (80% Train, 20% Test)
    split_idx = int(len(df_train_ready) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f" Entrenando Random Forest con {len(X_train)} epochs históricos...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X_train, y_train)

    print(" Evaluando modelo (Backtesting)...")
    y_pred_pct = model.predict(X_test)

    # Reconstrucción de la dificultad absoluta para métricas legibles
    prev_diff_test = df_train_ready['difficulty'].iloc[split_idx - 1:-1].values
    real_diff_test = df_train_ready['difficulty'].iloc[split_idx:].values
    predicted_diff_absolute = prev_diff_test * (1 + y_pred_pct)

    mae = mean_absolute_error(real_diff_test, predicted_diff_absolute)
    mape = mean_absolute_percentage_error(real_diff_test, predicted_diff_absolute) * 100

    # --- EXPORTACIÓN DE RESULTADOS ---
    print(" Guardando artefactos del modelo en la carpeta model/ ...")

    # 1. Guardar el modelo entrenado
    joblib.dump(model, MODEL_OUTPUT)

    # 2. Guardar métricas y metadatos de las features
    feature_importances = dict(zip(features, model.feature_importances_.tolist()))
    metrics_data = {
        "mae": float(mae),
        "mape": float(mape),
        "feature_importances": feature_importances
    }
    with open(METRICS_OUTPUT, 'w') as f:
        json.dump(metrics_data, f, indent=4)

    # 3. Guardar datos de backtesting para la gráfica del dashboard
    test_dates = df_train_ready['date'].iloc[split_idx:].dt.strftime('%Y-%m-%d').tolist()
    backtest_data = {
        "dates": test_dates,
        "real_diff": real_diff_test.tolist(),
        "predicted_diff": predicted_diff_absolute.tolist()
    }
    with open(BACKTEST_OUTPUT, 'w') as f:
        json.dump(backtest_data, f)

    print(f"Proceso completado con éxito MAPE: {mape:.2f}%")


if __name__ == "__main__":
    train_and_evaluate()