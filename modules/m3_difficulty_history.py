"""Advanced implementation for module M3."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api.blockchain_client import get_exact_difficulty_history

def render() -> None:
    """Render the M3 panel with DAA audit and step charts."""
    st.header("M3 - Difficulty History & DAA Audit")
    st.write("Análisis forense del Algoritmo de Ajuste de Dificultad (DAA) y los límites de seguridad del protocolo.")

    timespan_options = {"1 Año": "1year", "2 Años": "2years", "Todo el Historial": "all"}
    selected_timespan = st.selectbox("Selecciona el rango temporal", list(timespan_options.keys()), index=1)

    if st.button("Auditar Historial de Ajustes", type="primary", key="m3_load"):
        with st.spinner("Descargando y procesando epochs..."):
            try:
                # 1. Extracción de datos sin muestreo
                raw_values = get_exact_difficulty_history(timespan_options[selected_timespan])

                # PROTECCIÓN: Manejo elegante de errores como pide el proyecto
                if not raw_values:
                    st.warning(
                        "La API de Blockchain.info está limitando el tráfico temporalmente (Rate Limit). Por favor, espera unos segundos e inténtalo de nuevo.")
                    return  # Salimos de la función para no romper Pandas

                df = pd.DataFrame(raw_values)
                df = df.rename(columns={"x": "timestamp", "y": "difficulty"})

                # 2. Procesamiento Matemático: Detectar Epochs
                # Un nuevo epoch comienza cuando la dificultad cambia respecto al valor anterior
                df['prev_diff'] = df['difficulty'].shift(1)
                epochs = df[df['difficulty'] != df['prev_diff']].copy()

                # Limpieza y cálculos de tiempo
                epochs['date'] = pd.to_datetime(epochs['timestamp'], unit="s")
                epochs['time_elapsed_sec'] = epochs['timestamp'].diff()
                epochs['time_elapsed_days'] = epochs['time_elapsed_sec'] / 86400

                # Descartar la primera fila (no tiene epoch anterior para comparar)
                epochs = epochs.dropna(subset=['time_elapsed_sec']).reset_index(drop=True)

                # 3. Auditoría del Algoritmo (DAA)
                # Fórmula: Diff_nueva = Diff_anterior * (Tiempo Objetivo / Tiempo Real)
                target_time_sec = 2016 * 600  # 1,209,600 segundos (14 días exactos)

                epochs['calculated_new_diff'] = epochs['prev_diff'] * (target_time_sec / epochs['time_elapsed_sec'])

                # Limitar por el 4x Cap de seguridad (Max 400%, Min 25%)
                epochs['max_allowed'] = epochs['prev_diff'] * 4
                epochs['min_allowed'] = epochs['prev_diff'] / 4

                # Recalcular aplicando los límites teóricos del protocolo
                epochs['theoretical_diff'] = epochs[['calculated_new_diff', 'max_allowed']].min(axis=1)
                epochs['theoretical_diff'] = epochs[['theoretical_diff', 'min_allowed']].max(axis=1)

                # --- VISUALIZACIÓN 1: GRÁFICO ESCALONADO ---
                st.subheader("Evolución de la Dificultad (Step Chart)")

                fig = go.Figure()

                # Línea real de dificultad (hv = horizontal-vertical para formar escalones)
                fig.add_trace(go.Scatter(
                    x=epochs['date'],
                    y=epochs['difficulty'],
                    mode='lines',
                    line_shape='hv',
                    name='Dificultad Real de la Red',
                    line=dict(color='#f2a900', width=3)
                ))

                fig.update_layout(
                    title="Historial de Ajustes (Múltiplos de 2016 Bloques)",
                    xaxis_title="Fecha del Ajuste",
                    yaxis_title="Dificultad",
                    hovermode="x unified"
                )

                st.plotly_chart(fig, width='stretch')

                st.markdown("---")

                # --- VISUALIZACIÓN 2: AUDITORÍA MATEMÁTICA ---
                st.subheader("Auditoría del Ajuste de Dificultad")
                st.info("Reconstruimos localmente las matemáticas del protocolo. Comparamos el tiempo real que tardaron en minarse los últimos 2016 bloques contra el objetivo teórico de 14 días (1,209,600 segundos) para verificar la precisión del ajuste.")

                # Preparar datos para la tabla de los últimos 5 ajustes
                recent_epochs = epochs.tail(5).copy()
                recent_epochs = recent_epochs.sort_values('date', ascending=False)

                display_df = pd.DataFrame({
                    "Fecha del Ajuste": recent_epochs['date'].dt.strftime('%Y-%m-%d %H:%M'),
                    "Días en minar (Epoch)": recent_epochs['time_elapsed_days'].round(2),
                    "Ratio (Real / 14D)": (recent_epochs['time_elapsed_days'] / 14).round(3),
                    "Dificultad Real": recent_epochs['difficulty'].apply(lambda x: f"{x:,.0f}"),
                    "Cálculo Teórico Local": recent_epochs['theoretical_diff'].apply(lambda x: f"{x:,.0f}")
                })

                st.dataframe(display_df, width='stretch', hide_index=True)

                # Check de integridad
                st.write("**Verificación de Integridad:** El 'Cálculo Teórico Local' aplica la fórmula del código fuente de Bitcoin `(Diff_anterior * 14_dias / Tiempo_real_epoch)` incluyendo los límites estrictos de aumento x4 y reducción /4. Si el código fuente se respeta, ambas columnas de dificultad deben ser prácticamente idénticas (salvo mínimos redondeos de red).")

            except Exception as exc:
                st.error(f"Error cargando o procesando el historial: {exc}")
    else:
        st.info("Haz clic en 'Auditar Historial' para procesar los epochs y cargar los gráficos.")