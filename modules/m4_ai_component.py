"""Advanced implementation for module M4 (AI Component)."""

import os
import json
import joblib
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def load_model_artifacts():
    """Carga el modelo preentrenado y sus métricas desde el disco."""
    current_dir = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(current_dir, "model", "rf_model.joblib")
    metrics_path = os.path.join(current_dir, "model", "metrics.json")
    backtest_path = os.path.join(current_dir, "model", "backtest_data.json")

    if not (os.path.exists(model_path) and os.path.exists(metrics_path) and os.path.exists(backtest_path)):
        st.error("Archivos del modelo no encontrados. Ejecuta `python model/train_model.py` primero.")
        st.stop()

    model = joblib.load(model_path)

    with open(metrics_path, 'r', encoding='utf-8') as f:
        metrics = json.load(f)

    with open(backtest_path, 'r', encoding='utf-8') as f:
        backtest_data = json.load(f)

    return model, metrics, backtest_data

def get_current_state():
    """Obtiene el último dato disponible para hacer la inferencia del futuro."""
    current_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(current_dir, "data", "difficulty.json")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df_diff = pd.DataFrame(data.get("difficulty", []))
    df_price = pd.DataFrame(data.get("market-price", []))

    # Solo necesitamos las dos últimas filas para calcular las variaciones (%)
    last_two_diff = df_diff.tail(2)['y'].values
    last_two_price = df_price.tail(2)['y'].values

    current_diff = last_two_diff[-1]
    prev_diff = last_two_diff[0]
    current_price = last_two_price[-1]
    prev_price = last_two_price[0]

    diff_change_pct = (current_diff - prev_diff) / prev_diff
    price_change_pct = (current_price - prev_price) / prev_price

    # Creamos el vector (X) exactamente igual que en el entrenamiento
    X_future = pd.DataFrame([{
        'difficulty': current_diff,
        'price': current_price,
        'diff_change_pct': diff_change_pct,
        'price_change_pct': price_change_pct
    }])

    return current_diff, X_future

def render() -> None:
    """Render the M4 panel with pre-trained ML models."""
    st.header("M4 - Motor Predictivo de IA (Random Forest)")
    st.write("Modelo de Machine Learning de producción entrenado (offline) con historial *on-chain* para predecir la tendencia del próximo ajuste de dificultad.")

    try:
        # 1. Cargar el "cerebro"
        model, metrics, backtest_data = load_model_artifacts()

        # 2. Inferencia (Real-Time)
        current_diff, X_future = get_current_state()

        # El modelo predice la variación porcentual esperada
        predicted_future_pct = model.predict(X_future)[0]
        next_diff_prediction = current_diff * (1 + predicted_future_pct)

        # ==========================================
        # RENDERIZADO DEL DASHBOARD (UI/UX)
        # ==========================================

        # --- SECCIÓN 1: KPIs Principales ---
        st.subheader("Proyección del Próximo Epoch")
        col1, col2, col3 = st.columns(3)

        col1.metric("Dificultad Actual", f"{current_diff:,.0f}")
        col2.metric("Dificultad Predicha (IA)", f"{next_diff_prediction:,.0f}", f"{predicted_future_pct * 100:.2f}% estimado")
        col3.metric("Precisión del Modelo (MAPE)", f"{100 - metrics['mape']:.2f}%", "- Margen de Error Histórico")

        st.markdown("---")

        # --- SECCIÓN 2: Gráfica de Backtesting ---
        st.subheader("Gráfica de Validación (Backtesting)")
        st.write("Visualización del desempeño del modelo durante la fase de evaluación (20% más reciente de la historia). Compara la predicción *offline* con la realidad.")

        fig_pred = go.Figure()

        # Línea Real
        fig_pred.add_trace(go.Scatter(
            x=backtest_data['dates'], y=backtest_data['real_diff'],
            mode='lines+markers', name='Dificultad Real',
            line=dict(color='#f2a900', width=2)
        ))

        # Línea de Predicción (IA)
        fig_pred.add_trace(go.Scatter(
            x=backtest_data['dates'], y=backtest_data['predicted_diff'],
            mode='lines', name='Predicción de IA',
            line=dict(color='#00d2ff', width=2, dash='dot')
        ))

        fig_pred.update_layout(xaxis_title="Fecha", yaxis_title="Dificultad", hovermode="x unified")
        st.plotly_chart(fig_pred, width='stretch')

        st.markdown("---")

        # --- SECCIÓN 3: Explicabilidad y Transparencia ---
        col_expl1, col_expl2 = st.columns([1, 1])

        with col_expl1:
            st.subheader("Rendimiento Estadístico")
            st.info(f"**Error Absoluto Medio (MAE):** {metrics['mae']:,.0f} unidades.")
            st.write(f"El modelo tiene una desviación promedio de **{metrics['mape']:.2f}%** por predicción.")
            st.write("Al obligar a la IA a predecir *variaciones porcentuales (Deltas)* en lugar de números brutos, el **Random Forest** es capaz de extrapolar tendencias de crecimiento sin sufrir problemas de sobreajuste (overfitting).")

        with col_expl2:
            st.subheader("Importancia de Variables (Feature Importance)")

            # Extraemos los diccionarios de las métricas
            feat_names = list(metrics['feature_importances'].keys())
            feat_values = list(metrics['feature_importances'].values())

            # Gráfico de barras horizontal nativo de Plotly
            fig_imp = go.Figure(go.Bar(
                x=feat_values,
                y=['Dificultad Absoluta', 'Precio Absoluto', 'Variación Diff (%)', 'Variación Precio (%)'],
                orientation='h',
                marker=dict(color='#00d2ff')
            ))
            fig_imp.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=200, xaxis_title="Peso de la Variable (0 a 1)")
            st.plotly_chart(fig_imp, width='stretch')

        with st.expander("Ver documentación técnica (Explicación para el README)"):
            st.markdown("""
            ### Arquitectura de Producción (MLOps)
            Este módulo implementa un enfoque profesional separando la fase de entrenamiento (Offline) de la inferencia (Online).
            
            1. **Entrenamiento (`model/train_model.py`):** Un ensamble **Random Forest Regressor** de `scikit-learn` se entrenó con los datos históricos, exportando los pesos (`.joblib`) y las métricas (`.json`).
            2. **Inferencia (Dashboard):** Esta interfaz carga el modelo precongelado, garantizando respuestas en milisegundos sin sobrecargar el servidor con re-entrenamientos innecesarios.
            
            **Target Transformation:** El modelo no predice la dificultad absoluta, sino la variación porcentual del próximo ajuste, permitiendo proyectar el crecimiento exponencial característico de la red Bitcoin sin errores de extrapolación.
            """)

    except Exception as exc:
        st.error(f"Error cargando los artefactos de Inteligencia Artificial: {exc}")