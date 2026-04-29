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
| Chosen AI Approach | Random Forest Regressor time-series predictor using target transformation (predicting % change). Implemented with an MLOps architecture separating offline training from real-time online inference. |

## Module Tracking

Use one of these values: `Not started`, `In progress`, `Done`

| Module | What it should include | Status      |
|---|---|-------------|
| M1 | Proof of Work Monitor | Done        |
| M2 | Block Header Analyzer | Done        |
| M3 | Difficulty History | Done        |
| M4 | AI Component | Done        |

## Current Progress

- Upgraded `api/blockchain_client.py` with helpers for current difficulty, recent blocks, and exact difficulty history with API fallback to local JSON data.
- Completed M1 in `modules/m1_pow_monitor.py` with live PoW KPIs, reward/fees analysis, target-vs-hash checks, and statistical block interval visualization.
- Completed M2 in `modules/m2_block_header.py` with 80-byte header reconstruction (little-endian), double SHA-256 verification, and local CPU benchmark.
- Completed M3 in `modules/m3_difficulty_history.py` with DAA audit charts, epoch timing analysis, and theoretical-vs-real difficulty comparison.
- **Completed M4 in `modules/m4_ai_component.py` and `model/train_model.py`.** Built a Random Forest Regressor to predict difficulty adjustments. Separated offline training (exporting `.joblib` and metrics) from online inference to ensure millisecond load times. The model achieves a highly accurate MAPE of 2.66% by predicting percentage deltas rather than absolute values to avoid overfitting.

## Next Step

- Project is fully complete, tested, and ready for final submission and evaluation. 

## Main Problem or Blocker

- None. The previous technical risk regarding API rate limiting was completely mitigated by implementing a robust local fallback mechanism and decoupling the ML training process from the live dashboard.

<!-- student-repo-auditor:teacher-feedback:start -->
## Teacher Feedback

### Kick-off Review

Review time: 2026-04-29 20:31 CEST
Status: Green

Strength:
- I can see the dashboard structure integrating the checkpoint modules.

Improve now:
- The checkpoint evidence is strong: the dashboard and core modules are visibly progressing.

Next step:
- Keep building on this checkpoint and prepare the final AI integration.
<!-- student-repo-auditor:teacher-feedback:end -->
