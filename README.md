[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/N3kLi3ZO)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23640640&assignment_repo_type=AssignmentRepo)
# Blockchain Dashboard Project

Use this repository to build your blockchain dashboard project.
Update this README every week.

## Student Information

| Field              | Value |
|--------------------|---|
| Student Name       | Rodrigo Pérez Campesino |
| GitHub Username    | rperecam |
| Project Title      | CryptoChain Analyzer Dashboard |
| Chosen AI Approach | Predictor: Predict the next difficulty adjustment value using a time-series model |

## Module Tracking

Use one of these values: `Not started`, `In progress`, `Done`

| Module | What it should include | Status |
|---|---|---|
| M1 | Proof of Work Monitor | Done |
| M2 | Block Header Analyzer | Not started |
| M3 | Difficulty History | Not started |
| M4 | AI Component | Not started |

## Current Progress

Write 3 to 5 short lines about what you have already done.

- Updated `api/blockchain_client.py` with new helper functions to fetch current difficulty and recent blocks in a single workflow.
- Improved `modules/m1_pow_monitor.py` with advanced PoW analytics: estimated hash rate, block reward/fees breakdown, and target vs hash visualization.
- Added statistical analysis in M1 with a histogram of block intervals and a theoretical Poisson distribution overlay.
- Updated `requirements.txt` to include `fastapi` for upcoming backend/API integration.

## Next Step

Write the next small step you will do before the next class.

- Start implementing M2 (Block Header Analyzer) to extend the dashboard with deeper header-level validation metrics.

## Main Problem or Blocker

Write here if you are stuck with something.

- None at the moment; the initial GitHub setup and first API call are functioning correctly.

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
