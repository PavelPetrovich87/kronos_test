# Implementation Plan: Model Integration

**Branch**: `003-model-integration` | **Date**: 2026-01-19 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-model-integration/spec.md`

## Summary

Integrate the real `KronosModel` using PyTorch, enabling the strategy to generate signals from actual model predictions. Support both local execution (Mac/CPU/MPS) and Google Colab (Linux/GPU) via dynamic environment detection and path handling. Introduce a `StrategyFactory` to easily switch between Mock and Real modes.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: `torch`, `transformers`, `pandas`, `numpy`.
**Storage**: N/A (Read-only model weights).
**Testing**: `pytest` for unit/integration tests.
**Target Platform**: Local Mac (MPS/CPU) and Google Colab (Linux/CUDA).
**Project Type**: Python Research/Strategy Library
**Performance Goals**: Local inference < 60s (CPU) or < 5s (GPU) for 100 points.
**Constraints**: Must detect environment (Colab vs Local) to resolve paths correctly. `Kronos` repo expected as sibling directory. **No external inference API available**; Model must run embedded within the application process.
**Scale/Scope**: Single model instance.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Reproducible Notebooks**: Colab support explicitly handled.
- [x] **II. Data Immutability**: Model reading only.
- [x] **III. Risk-Adjusted**: N/A for model loading, but Strategy integration respects existing risk modules.
- [x] **IV. Modular Components**: Logic encapsulated in `lib/kronos_model.py` and `lib/strategy_factory.py`.
- [x] **V. Experiment Tracking**: Config used for model loading will be part of backtest results (existing pattern).
- [x] **VI. Standardized Layout**: Adheres to `lib/` structure.

## Project Structure

### Documentation (this feature)

```text
specs/003-model-integration/
├── plan.md              # This file
├── research.md          # Environment & Path decisions
├── data-model.md        # ModelConfig, Prediction entities
├── quickstart.md        # Colab & Local usage guide
├── contracts/           # N/A
└── tasks.md             # To be generated
```

### Source Code (repository root)

```text
lib/
├── kronos_model.py      # [MODIFY] Add environment detection, robust imports
├── strategy_factory.py  # [NEW] Factory to switch modes (Mock/Real)
├── strategy.py          # [MODIFY] Accept predictor/signals from factory? Or factory returns Strategy instance?
└── data_loader.py       # [NO CHANGE expected]

tests/
├── test_kronos_model.py # [NEW] Integration tests for model loading
└── test_factory.py      # [NEW] Factory logic tests
```

**Structure Decision**: 
- `StrategyFactory` creates the appropriate strategy instance (or injects the predictor).
- `KronosModel` class in `lib/kronos_model.py` handles the low-level PyTorch/HuggingFace interaction.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Verification Plan

### Automated Tests
- `pytest tests/test_factory.py`: Verify factory returns correct class based on config.
- `pytest tests/test_kronos_model.py`: Verify `KronosModel` can import `Kronos` repo (mocked path) and run `generate_signals` (mocked internal model).

### Manual Verification
1. **Local Real Run**: Run `verify_quickstart.py` with `mode="real"` on local machine. Confirm it loads model (slow on CPU is fine) and produces signals.
2. **Colab Run**: Create a temporary notebook, clone repos, and run `verify_quickstart.py`. Confirm `cuda` is used if available.
