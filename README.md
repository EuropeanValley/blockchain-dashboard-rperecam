[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/N3kLi3ZO)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23640640&assignment_repo_type=AssignmentRepo)
# Blockchain Dashboard Project

Use this repository to build your blockchain dashboard project.
Update this README every week.

## Student Information

| Field              | Value |
|--------------------|---|
| Student Name       | Rodrigo PÃ©rez Campesino |
| GitHub Username    | rperecam |
| Project Title      | CryptoChain Analyzer Dashboard |
| Chosen AI Approach | Predictor: Predict the next difficulty adjustment value using a time-series model |

## Module Tracking

Use one of these values: `Not started`, `In progress`, `Done`

| Module | What it should include | Status      |
|---|---|-------------|
| M1 | Proof of Work Monitor | Done        |
| M2 | Block Header Analyzer | Done        |
| M3 | Difficulty History | In progress |
| M4 | AI Component | Not started |

## Current Progress

Write 3 to 5 short lines about what you have already done.

- Implemented `modules/m2_block_header.py` with block header reconstruction in little-endian format, double SHA-256 validation, and a memory map of the 80-byte header.
- Connected M2 in `app.py` so the dashboard now exposes the Block Header Analyzer as a dedicated tab.
- Added a local benchmark in M2 to compare CPU hashing performance with Bitcoin mining context.
- Kept the recent improvements in `api/blockchain_client.py` and M1 as the foundation for the next dashboard modules.

## Next Step

Write the next small step you will do before the next class.


## Main Problem or Blocker

Write here if you are stuck with something.

- None at the moment; the initial GitHub setup and first API call are functioning correctly.

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
