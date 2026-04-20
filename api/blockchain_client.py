"""
Blockchain API client.

Provides helper functions to fetch blockchain data from public APIs.
"""

import requests
import time

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
