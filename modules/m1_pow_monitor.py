"""Advanced implementation for module M1."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from api.blockchain_client import get_latest_block, get_block, get_current_difficulty, get_recent_blocks_data

def bits_to_target_hex(bits: int) -> str:
    """Descomprime el campo 'bits' en el Target objetivo de 256 bits."""
    bits_hex = hex(bits)[2:]
    if len(bits_hex) % 2 != 0:
        bits_hex = '0' + bits_hex
    exponent = int(bits_hex[:2], 16)
    coefficient = int(bits_hex[2:], 16)
    target = coefficient * 2**(8 * (exponent - 3))
    return f"{target:064x}"

def render() -> None:
    """Render the M1 panel with analytical depth."""
    st.header("M1 - Proof of Work Monitor")
    st.write("Análisis en tiempo real del estado de minería de la red Bitcoin, carga criptográfica e incentivos.")

    if st.button("Actualizar Métricas de Red", type="primary", key="m1_fetch"):
        with st.spinner("Analizando la cadena de bloques..."):
            try:
                # 1. Extracción de datos
                latest_summary = get_latest_block()
                latest_block = get_block(latest_summary["hash"])
                diff_val = get_current_difficulty()
                recent_blocks = get_recent_blocks_data()

                # 2. Cálculos derivados (Hash Rate)
                hash_rate_hashes = (diff_val * (2**32)) / 600
                hash_rate_ehs = hash_rate_hashes / 1e18

                # 3. Cálculos de Economía (Block Reward)
                # En 2026, el subsidio por bloque es de 3.125 BTC tras el halving de 2024
                subsidy_btc = 3.125
                fee_satoshis = latest_block.get("fee", 0)
                fee_btc = fee_satoshis / 10**8
                total_reward_btc = subsidy_btc + fee_btc

                # --- RENDERIZADO DE LA INTERFAZ ---

                # Fila 1: KPIs Principales
                col1, col2, col3 = st.columns(3)
                col1.metric("Altura del Bloque", f"{latest_block.get('height'):,}")
                col2.metric("Dificultad Actual", f"{diff_val:,.0f}")
                col3.metric("Hash Rate Estimado", f"{hash_rate_ehs:.2f} EH/s")

                st.markdown("---")

                # Fila 2: Economía e Incentivos (¡NUEVO!)
                st.subheader("Economía del Bloque e Incentivos")
                ec1, ec2, ec3 = st.columns(3)
                ec1.metric("Recompensa Total", f"{total_reward_btc:.4f} BTC")
                ec2.metric("Comisiones (Fees)", f"{fee_btc:.4f} BTC")
                ec3.metric("Peso de las Comisiones", f"{(fee_btc/total_reward_btc)*100:.2f} %")

                st.info(" **El incentivo de la seguridad:** Los mineros consumen energía (PoW) a cambio de esta recompensa. A medida que el subsidio fijo disminuye cada 4 años (halvings), las comisiones de red deben compensar el coste de mantener el Hash Rate alto para evitar ataques del 51%.")

                st.markdown("---")

                # Fila 3: Criptografía - Espacio SHA-256
                st.subheader("Verificación Visual del Proof of Work")
                bits = latest_block.get("bits", 0)
                target_hex = bits_to_target_hex(bits)
                block_hash = latest_block.get("hash", "")

                st.code(f"Target: {target_hex}\nHash:   {block_hash}", language="text")

                # Explicación Avanzada del Nonce (¡NUEVO!)
                with st.expander("Análisis Profundo: La paradoja del Nonce de 32-bits", expanded=False):
                    st.write(f"El campo `nonce` de la cabecera es el valor ganador que logró este hash: **`{latest_block.get('nonce')}`**.")
                    st.write("Sin embargo, el espacio del nonce está limitado a $2^{32}$ (aprox. 4.29 mil millones de combinaciones). Dado el Hash Rate actual de la red, un solo minero ASIC agota todas las combinaciones posibles en una fracción de segundo.")

                    st.latex(r"Tiempo_{agotamiento} = \frac{2^{32}}{\text{Hash Rate actual}}")

                    st.write("Por lo tanto, iterar el Nonce **no es suficiente**. Los mineros modernos deben modificar constantemente la transacción *Coinbase* (añadiendo un *ExtraNonce*). Esto altera la raíz de Merkle (`merkle_root`) en la cabecera, generando un espacio de búsqueda de hash completamente nuevo cada vez que el Nonce principal se desborda.")

                st.markdown("---")

                # Fila 4: Análisis de la Distribución del Tiempo
                st.subheader("Distribución Estadística del Tiempo entre Bloques")

                if recent_blocks:
                    df = pd.DataFrame(recent_blocks)
                    df = df.sort_values(by="time").reset_index(drop=True)
                    df["time_diff"] = df["time"].diff()
                    df = df.dropna()

                    fig = px.histogram(
                        df,
                        x="time_diff",
                        nbins=25,
                        labels={"time_diff": "Segundos entre bloques", "count": "Frecuencia"},
                        opacity=0.75
                    )

                    lam = 1 / 600
                    x_range = np.linspace(0, df["time_diff"].max(), 100)
                    y_exp = lam * np.exp(-lam * x_range)

                    bin_width = df["time_diff"].max() / 25
                    y_scaled = y_exp * len(df) * bin_width

                    fig.add_trace(go.Scatter(
                        x=x_range,
                        y=y_scaled,
                        mode='lines',
                        name='Distribución Teórica',
                        line=dict(color='#ff4b4b', width=3)
                    ))

                    fig.update_layout(
                        title=f"Muestra de los últimos {len(df)} bloques minados",
                        showlegend=True,
                        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
                    )

                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("La línea roja representa un Proceso de Poisson teórico ($f(x) = \lambda e^{-\lambda x}$), evidenciando que la minería carece de memoria.")

            except Exception as exc:
                st.error(f"Error procesando la arquitectura de datos: {exc}")
    else:
        st.info("Inicia la sincronización para analizar el estado actual de la red.")