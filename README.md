[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/N3kLi3ZO)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23640640&assignment_repo_type=AssignmentRepo)
# Blockchain Dashboard Project

Use this repository to build your blockchain dashboard project.
Update this README every week.

## Student Information

| Field              | Value |
|--------------------|---|
| Student Name       | Rodrigo Perez Campesino |
| GitHub Username    | rperecam |
| Project Title      | CryptoChain Analyzer Dashboard |
| Chosen AI Approach | Time-series predictor to estimate the next Bitcoin difficulty adjustment using recent historical data; output includes predicted value and MAE. |

## Module Tracking

Use one of these values: `Not started`, `In progress`, `Done`

| Module | What it should include | Status      |
|---|---|-------------|
| M1 | Proof of Work Monitor | Done        |
| M2 | Block Header Analyzer | Done        |
| M3 | Difficulty History | Done        |
| M4 | AI Component | Not started |

## Current Progress

- Upgraded `api/blockchain_client.py` with helpers for current difficulty, recent blocks, and exact difficulty history with API fallback to local JSON data.
- Completed M1 in `modules/m1_pow_monitor.py` with live PoW KPIs, reward/fees analysis, target-vs-hash checks, and statistical block interval visualization.
- Completed M2 in `modules/m2_block_header.py` with 80-byte header reconstruction (little-endian), double SHA-256 verification, and local CPU benchmark.
- Completed M3 in `modules/m3_difficulty_history.py` with DAA audit charts, epoch timing analysis, and theoretical-vs-real difficulty comparison.
- Integrated M1-M4 tabs in `app.py` and updated `requirements.txt` to include `fastapi` for upcoming API/backend work.

## Next Step

- Start M4 by building a baseline AI predictor (time-series or linear regression), show real vs predicted difficulty, and report MAE in the dashboard.

## Main Problem or Blocker

- Main technical risk is API rate limiting for historical data; fallback loading already works, and the next improvement is adding cache to reduce requests.
## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

<!-- student-repo-auditor:teacher-feedback:start -->
## Teacher Feedback

### Kick-off Review

Review time: 2026-04-21 09:20 CEST
Status: Amber

Strength:
- Your repository keeps the expected classroom structure.

Improve now:
- The README is present but still misses part of the required kickoff information.

Next step:
- Complete the README fields for student information, AI approach, module status, and next step.
<!-- student-repo-auditor:teacher-feedback:end -->
