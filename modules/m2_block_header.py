"""Advanced implementation for module M2."""

import streamlit as st
import hashlib
import struct
import time

from api.blockchain_client import get_latest_block, get_block

def get_little_endian_hex(value: int | str, is_hex: bool = False) -> str:
    """Convierte valores al formato Little-Endian."""
    if is_hex:
        return bytes.fromhex(str(value))[::-1].hex()
    else:
        return struct.pack('<I', int(value)).hex()

def render() -> None:
    """Render the M2 panel with memory mapping and hardware benchmarking."""
    st.header("M2 - Block Header Analyzer")
    st.write("Verificación criptográfica de bajo nivel y arquitectura de memoria del bloque.")

    try:
        default_hash = st.session_state.get('latest_hash_m2', "")
        if not default_hash:
            latest = get_latest_block()
            default_hash = latest.get("hash", "")
            st.session_state['latest_hash_m2'] = default_hash
    except Exception:
        default_hash = ""

    block_hash = st.text_input(
        "Block Hash",
        value=default_hash,
        key="m2_hash",
        help="Introduce el hash de un bloque para descargar su cabecera y auditarla localmente."
    )

    # Inicializar el estado de la memoria si no existe
    if 'header_audited_hash' not in st.session_state:
        st.session_state['header_audited_hash'] = None

    # Botón principal: Solo actualiza la memoria
    if st.button("Auditar Cabecera", type="primary", key="m2_lookup") and block_hash:
        st.session_state['header_audited_hash'] = block_hash

    # Si la memoria coincide con el hash en pantalla, dibujamos todo (así sobrevive a las recargas)
    if st.session_state.get('header_audited_hash') == block_hash:
        with st.spinner("Ensamblando bytes y calculando hashes..."):
            try:
                block = get_block(block_hash)

                version = block.get('ver')
                prev_block = block.get('prev_block')
                mrkl_root = block.get('mrkl_root')
                time_val = block.get('time')
                bits = block.get('bits')
                nonce = block.get('nonce')

                ver_le = get_little_endian_hex(version)
                prev_le = get_little_endian_hex(prev_block, is_hex=True)
                mrkl_le = get_little_endian_hex(mrkl_root, is_hex=True)
                time_le = get_little_endian_hex(time_val)
                bits_le = get_little_endian_hex(bits)
                nonce_le = get_little_endian_hex(nonce)

                header_hex = ver_le + prev_le + mrkl_le + time_le + bits_le + nonce_le
                header_bytes = bytes.fromhex(header_hex)

                # --- SECCIÓN 1: MAPA DE MEMORIA ---
                st.subheader("1. Mapa de Memoria de la Cabecera (80 Bytes)")
                st.info("La cabecera de Bitcoin está optimizada al milímetro. Observa cómo los datos criptográficos dominan la estructura.")

                col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns([1, 8, 8, 1, 1, 1])
                col_m1.metric("Ver", "4B")
                col_m2.metric("Prev. Hash", "32B")
                col_m3.metric("Merkle Root", "32B")
                col_m4.metric("Time", "4B")
                col_m5.metric("Bits", "4B")
                col_m6.metric("Nonce", "4B")

                with st.expander("Ver volcado hexadecimal completo (Little-Endian)"):
                    st.code(f"[{ver_le}]-[{prev_le}]-[{mrkl_le}]-[{time_le}]-[{bits_le}]-[{nonce_le}]", language="text")
                    st.write("**Payload Final Concatenado:**")
                    st.code(header_hex, language="text")

                st.markdown("---")

                # --- SECCIÓN 2: VERIFICACIÓN MATEMÁTICA ---
                st.subheader("2. Motor de Validación $\\text{SHA-256}$")

                hash1 = hashlib.sha256(header_bytes).digest()
                hash2 = hashlib.sha256(hash1).digest()
                calculated_hash = hash2[::-1].hex()

                binary_str = bin(int(calculated_hash, 16))[2:].zfill(256)
                zero_bits = len(binary_str) - len(binary_str.lstrip('0'))

                col_res1, col_res2 = st.columns(2)
                col_res1.write("**Fórmula aplicada localmente:**")
                col_res1.latex(r"\text{Hash} = \text{SHA256}(\text{SHA256}(\text{Header}_{80B}))")

                if calculated_hash == block_hash:
                    col_res2.success(f"**Verificación Exitosa**\n\nEl hash calculado coincide. Encontramos **{zero_bits} bits** a cero.")
                else:
                    col_res2.error("Los hashes no coinciden. Posible corrupción de datos.")

                st.code(f"Hash Oficial : {block_hash}\nCalculado    : {calculated_hash}", language="text")

                st.markdown("---")

                # --- SECCIÓN 3: BENCHMARK DE HARDWARE ---
                st.subheader("3. Hardware Profiling: Python CPU vs. Red Bitcoin")
                st.write("Mide el rendimiento criptográfico de tu máquina ejecutando un bucle de minería simulado durante 1 segundo.")

                # Ahora este botón funciona porque no está anidado lógicamente bajo la acción de pulsado del primero
                if st.button("Ejecutar Benchmark Local", key="run_bench"):
                    with st.spinner("Estresando CPU local durante 1 segundo..."):
                        start_time = time.time()
                        hashes_calculated = 0

                        while time.time() - start_time < 1.0:
                            hashlib.sha256(hashlib.sha256(header_bytes).digest()).digest()
                            hashes_calculated += 1

                        st.success(f"Benchmark completado: Tu entorno procesó **{hashes_calculated:,} H/s**.")

                        asic_hs = 100 * 10**12
                        ratio = asic_hs / hashes_calculated if hashes_calculated > 0 else 0

                        st.warning(f"**Contexto Cuantitativo:** Un solo minero ASIC moderno (ej. Antminer S19) genera aprox. 100 Terahashes por segundo. Tu ordenador tardaría unos **{ratio:,.0f} segundos** en hacer el trabajo que un ASIC hace en un solo segundo.")

            except Exception as exc:
                st.error(f"Error procesando la arquitectura de datos: {exc}")
    elif not block_hash:
        st.info("Inicia la auditoría ingresando un Block Hash.")