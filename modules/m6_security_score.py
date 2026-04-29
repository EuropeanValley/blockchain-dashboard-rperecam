"""Advanced implementation for module M6 (Security Score)."""

import math
import streamlit as st
import plotly.graph_objects as go
from api.blockchain_client import get_current_difficulty


def attacker_success_probability(q: float, z: int) -> float:
    """
    Implementación en Python de la fórmula en C de Satoshi Nakamoto (Whitepaper §11).
    Calcula la probabilidad de que un atacante con un % de hash rate (q)
    pueda reescribir una transacción que tiene 'z' confirmaciones.
    """
    p = 1.0 - q
    if q >= p:
        return 1.0

    lam = z * (q / p)
    sum_prob = 0.0

    for k in range(z + 1):
        poisson = math.exp(-lam) * (lam ** k) / math.factorial(k)
        prob = poisson * (1 - (q / p) ** (z - k))
        sum_prob += prob

    return 1.0 - sum_prob


def render() -> None:
    """Render the M6 panel with attack cost estimation and Nakamoto probability."""
    st.header("M6 - Security Score (Análisis de Ataque del 51%)")
    st.write(
        "Evaluación del modelo de seguridad económica de Bitcoin y la resistencia matemática frente a reorganizaciones de cadena.")

    try:
        with st.spinner("Calculando la entropía actual de la red..."):
            # Obtener dificultad actual para derivar el Hash Rate real
            diff_val = get_current_difficulty()

            # Hash Rate actual en la red (Hashes/segundo)
            current_hashrate_hps = (diff_val * (2 ** 32)) / 600
            current_hashrate_ehs = current_hashrate_hps / 1e18

            # Para conseguir el 51% del total, el atacante necesita superar al 100% actual.
            # Matemáticamente: Ha / (H_actual + Ha) = 0.51 -> Ha = 1.04 * H_actual
            attacker_hashrate_needed = current_hashrate_hps * 1.04
            attacker_ehs = attacker_hashrate_needed / 1e18

            # --- SECCIÓN 1: COSTE DEL ATAQUE DEL 51% ---
            st.subheader("1. Coste Operativo del Ataque del 51% (Hardware & Energía)")
            st.info(
                "Para reescribir el historial de transacciones, un atacante debe aportar más poder de cálculo que toda la red combinada.")

            col_sliders, col_metrics = st.columns([1, 1.5])

            with col_sliders:
                st.write("**Parámetros del Atacante:**")
                # Eficiencia media de un Antminer S19 XP es ~21.5 J/TH
                asic_efficiency = st.slider("Eficiencia del Hardware (Joules/TH)", min_value=10.0, max_value=50.0,
                                            value=21.5, step=0.5,
                                            help="Cuanto menor, más moderno y eficiente es el hardware minero.")
                # Coste medio industrial de electricidad en USD
                energy_cost_kwh = st.slider("Coste de Electricidad ($/kWh)", min_value=0.01, max_value=0.20, value=0.05,
                                            step=0.01)

            with col_metrics:
                # Cálculos de consumo y coste
                # Watts = (Hashes/s / 1e12) * J/TH
                power_needed_watts = (attacker_hashrate_needed / 1e12) * asic_efficiency
                power_needed_gw = power_needed_watts / 1e9  # Gigawatts

                cost_per_hour = (power_needed_watts / 1000) * energy_cost_kwh

                st.metric("Poder de Cómputo Requerido", f"{attacker_ehs:.2f} EH/s")
                st.metric("Consumo Eléctrico Continuo", f"{power_needed_gw:.2f} Gigavatios (GW)",
                          "Equivalente a varios reactores nucleares")
                st.metric("Coste de Energía por Hora", f"${cost_per_hour:,.0f} USD / hora")

            st.write(
                f"*Nota:* Este cálculo **solo asume el coste eléctrico**. Adquirir {attacker_ehs:.2f} EH/s en máquinas ASIC modernas costaría decenas de miles de millones de dólares y excedería la capacidad de fabricación global de semiconductores de TSMC.")

            st.markdown("---")

            # --- SECCIÓN 2: PROBABILIDAD DE NAKAMOTO (CONFIRMACIONES) ---
            st.subheader("2. Profundidad de Confirmaciones (Nakamoto 2008, §11)")
            st.write(
                "Incluso si un atacante consigue una gran cantidad de Hash Rate (sin llegar al 51%), ¿cuál es la probabilidad de que logre alterar un pago si el vendedor espera 'Z' confirmaciones?")

            # Generar datos para la gráfica
            z_values = list(range(0, 11))  # De 0 a 10 bloques (confirmaciones)
            q_values = [0.10, 0.20, 0.30, 0.40]  # 10%, 20%, 30% y 40% del hash rate total

            fig = go.Figure()

            for q in q_values:
                probabilities = [attacker_success_probability(q, z) * 100 for z in z_values]
                fig.add_trace(go.Scatter(
                    x=z_values,
                    y=probabilities,
                    mode='lines+markers',
                    name=f'Atacante tiene {int(q * 100)}% del Hash Rate'
                ))

            fig.update_layout(
                title="Probabilidad de éxito del atacante frente a confirmaciones (Z)",
                xaxis_title="Profundidad (Confirmaciones Z)",
                yaxis_title="Probabilidad de Éxito (%)",
                xaxis=dict(tickmode='linear', tick0=0, dtick=1),
                yaxis=dict(range=[0, 100]),
                hovermode="x unified",
                template="plotly_dark"
            )

            st.plotly_chart(fig, width='stretch')

            # Explicación Final
            st.success(
                "**Conclusión Criptográfica:** Como demuestra la gráfica, la probabilidad de fraude cae exponencialmente con cada nuevo bloque añadido a la cadena. Es por esto que los exchanges exigen 3 o 6 confirmaciones para depósitos grandes. El consenso Proof of Work se vuelve estadísticamente irreversible gracias a la asimetría termodinámica.")

    except Exception as exc:
        st.error(f"Error procesando los datos de seguridad: {exc}")