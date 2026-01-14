<!--
Sync Impact Report:
- Version change: 1.0.0 -> 1.1.0 (Added Standardized Layout)
- Modified principles: None
- Added sections: VI. Standardized Layout
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md (✅ Verified - Compatible)
  - .specify/templates/spec-template.md (✅ Verified - Compatible)
  - .specify/templates/tasks-template.md (✅ Verified - Compatible)
- Follow-up TODOs: None
-->
# Kronos Strategy Research Constitution

## Core Principles

### I. Reproducible Notebooks
Notebooks must be executable from top to bottom. No hidden state or out-of-order execution dependencies. Random seeds must be fixed.

### II. Data Immutability
Raw market data is immutable. All transformations must be explicit pipelines. Never overwrite source data. Data resides strictly in `data/`.

### III. Risk-Adjusted & Realistic
All strategy evaluations must account for transaction costs, slippage, and include risk metrics (Sharpe, Drawdown) alongside returns.

### IV. Modular Components
Complex logic and reusable strategy components must be extracted to library/utility files in `lib/`. Notebooks are for coordination and analysis, not heavy implementation.

### V. Experiment Tracking
Every strategy run must log its parameters, version, and key metrics to `results/`. We do not rely on "remembering" what config produced a result.

### VI. Standardized Layout
The project must adhere to the defined structure: `data/` (raw inputs), `lib/` (shared code), `notebooks/` (experiments), `results/` (artifacts), and `Kronos/` (base model). Root directory is for configuration only.

## Governance

- Amendments require a PR and reasoning.
- Constitution supersedes all other documentation.

**Version**: 1.1.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-01-14
