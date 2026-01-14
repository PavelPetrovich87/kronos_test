# Implementation Plan: Strategy Implementation

**Branch**: `002-strategy-implementation` | **Date**: 2026-01-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-strategy-implementation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement the Phase 3 strategy execution layer, which converts raw model predictions into actionable trade signals (Signal Generation), simulates their performance (Backtester), and applies safety controls (Risk Management). This feature bridges the gap between the `KronosModel` and actionable insights.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: `pandas` (DataFrames), `numpy` (calculations), `yfinance` (data source - already integrated), `kronos_model` (internal model - stubbed or real).
**Storage**: CSV/Parquet for backtest results and trade logs (in `results/` folder per Constitution).
**Testing**: `pytest` for unit and integration tests.
**Target Platform**: Local execution (Mac), future-proofed for Colab.
**Project Type**: Python Research/Strategy Library
**Performance Goals**: Backtester should process 1 year of hourly data < 5s.
**Constraints**: Must adhere to Data Immutability (never overwrite `data/`).
**Scale/Scope**: Single-asset strategy initially, extensible to portfolio.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Reproducible Notebooks**: Backtester logic will be in `lib/`, notebooks will call it with fixed params.
- [x] **II. Data Immutability**: Backtester reads from `data/` but writes only to `results/`.
- [x] **III. Risk-Adjusted**: Metrics module MUST include Sharpe and Drawdown.
- [x] **IV. Modular Components**: Strategy logic separated into `lib/strategy.py`, `lib/backtester.py`.
- [x] **V. Experiment Tracking**: Backtest results saved with timestamp and config.
- [x] **VI. Standardized Layout**: Adheres to `lib/`, `tests/` structure.

## Project Structure

### Documentation (this feature)

```text
specs/002-strategy-implementation/
├── plan.md              # This file
├── research.md          # Strategy choices
├── data-model.md        # Entities: Signal, Trade, BacktestResult
├── quickstart.md        # How to run backtests
├── contracts/           # N/A (Library-internal APIs)
└── tasks.md             # Task breakdown
```

### Source Code (repository root)

```text
lib/
├── strategy.py          # [NEW] Signal generation logic
├── backtester.py        # [MODIFY] Implement core backtest loop
├── reporting.py         # [NEW] Metric calculations (Sharpe, DD)
└── risk.py              # [NEW] Volatility checks

tests/
├── test_strategy.py     # [NEW] Unit tests for signals
├── test_backtester.py   # [NEW] Integration tests for engine
└── test_risk.py         # [NEW] Unit tests for risk limits
```

**Structure Decision**: Extending the existing single-project structure by adding specialized modules in `lib/` to keep notebooks clean (Constitution IV).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
