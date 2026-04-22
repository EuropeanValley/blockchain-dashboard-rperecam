"""
Blockchain API client.

Provides helper functions to fetch blockchain data from public APIs.
"""

import requests
import time
import json
import os

BASE_URL = "https://blockchain.info"


def get_latest_block() -> dict:
    """Return the latest block summary."""
    response = requests.get(f"{BASE_URL}/latestblock", timeout=10)
    response.raise_for_status()
    return response.json()


def get_block(block_hash: str) -> dict:
    """Return full details for a block identified by *block_hash*."""
    response = requests.get(
        f"{BASE_URL}/rawblock/{block_hash}", timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_difficulty_history(n_points: int = 100) -> list[dict]:
    """Return the last *n_points* difficulty values as a list of dicts."""
    response = requests.get(
        f"{BASE_URL}/charts/difficulty",
        params={"timespan": "1year", "format": "json", "sampled": "true"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("values", [])[-n_points:]


def get_current_difficulty() -> float:
    """Devuelve la dificultad actual de la red como un float."""
    response = requests.get(f"{BASE_URL}/q/getdifficulty", timeout=10)
    response.raise_for_status()
    return float(response.text)

def get_recent_blocks_data() -> list[dict]:
    """
    Obtiene los bloques minados en las últimas horas (usando el timestamp actual).
    Esencial para calcular la distribución temporal sin hacer decenas de llamadas API.
    """
    current_time_ms = int(time.time() * 1000)
    response = requests.get(f"{BASE_URL}/blocks/{current_time_ms}?format=json", timeout=10)
    response.raise_for_status()
    return response.json()

def get_exact_difficulty_history(timespan: str = "2years") -> list[dict]:
    """
    Obtiene el historial de dificultad con fallback a datos locales en caso de bloqueo WAF.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    # 1. Bucle de intentos optimizado: Petición exacta (false) y luego muestreada (true)
    for sampled in ["false", "true"]:
        try:
            response = requests.get(
                f"{BASE_URL}/charts/difficulty",
                params={"timespan": timespan, "format": "json", "sampled": sampled},
                headers=headers,
                timeout=5,  # Timeout rápido para no bloquear la UI
            )
            # Verificamos que la respuesta es válida y no un HTML del cortafuegos
            if response.status_code == 200 and response.text.strip().startswith('{'):
                return response.json().get("values", [])
        except requests.exceptions.RequestException:
            continue  # Fallo de red, pasamos al siguiente intento silenciosamente

    # 2. Si ambos intentos fallan, cargamos el fallback local
    print("API inaccesible. Cargando historial masivo desde data/difficulty.json...")

    try:
        # Construimos la ruta absoluta hacia la carpeta 'data' (subiendo un nivel desde 'api')
        current_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(current_dir, "data", "difficulty.json")

        with open(json_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        fallback_values = file_data.get("difficulty", [])

        # Convertimos los timestamps de ms a s para mantener la consistencia con la API
        for item in fallback_values:
            item["x"] = int(item["x"] / 1000)

        return fallback_values

    except Exception as e:
        print(f" Error crítico leyendo el JSON local: {e}")
        return []  # Devolvemos una lista vacía como último recurso para no lanzar un 500