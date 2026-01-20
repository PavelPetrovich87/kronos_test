# Implementation Plan: Test Command Center

**Branch**: `004-test-command-center` | **Date**: 2026-01-20 | **Spec**: [specs/004-test-command-center/spec.md](spec.md)
**Input**: Feature specification from `/specs/004-test-command-center/spec.md`

## Summary

Create a centralized Jupyter Notebook (`notebooks/Test_Command_Center.ipynb`) that acts as a researcher's cockpit. It will provide interactive parametric controls (widgets) for backtest settings and professional visualizations of performance. The technical approach involves moving complex plotting logic into a new `lib/visualizer.py` module and using `plotly` for zoomable charts. 

> [!IMPORTANT]
> **Performance Constraint**: All automated tests and notebook defaults will use a "Small Data" subset (e.g., last 100-500 bars) to ensure execution finishes in seconds on local CPUs.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: `pandas`, `numpy`, `plotly` (interactive charts), `ipywidgets` (parametric controls), `lib.kronos_model`, `lib.backtester`.  
**Storage**: Reading from `data/*.csv`, logging results to `results/*.json`.  
**Testing**: `pytest` for plotting data preparation and factory logic.  
**Target Platform**: Local Mac (Jupyter/VSCode) and Google Colab.
**Project Type**: Python Research/Strategy Library  
**Performance Goals**: Full rendering (Config -> Plot) in < 15s for 1 year of hourly data.  
**Constraints**: Must use `plotly` to ensure zoomability and cross-platform compatibility (Colab output).  
**Scale/Scope**: Single-symbol analysis for MVP.

## Cockpit Widget Breakdown

To provide the "insights" requested, the notebook cockpit will include the following `ipywidgets`:

| Widget Type | Parameter | Default | Description |
| :--- | :--- | :--- | :--- |
| **Dropdown** | `Symbol` | `BTC-USD` | Select which CSV data to load from `/data`. |
| **ToggleButtons** | `Mode` | `mock` | Switch between `mock` (fast/logic test) and `real` (AI Model). |
| **DateRangeSlider**| `Range` | Last 30 Days | Define the historical window for backtesting. |
| **FloatSlider** | `Threshold` | `0.01` | Confidence threshold for signal generation. |
| **FloatText`** | `Capital` | `10000.0` | Initial starting balance for the simulation. |
| **Button** | `Run` | N/A | Primary trigger to execute Predict -> Backtest -> Render. |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Reproducible Notebooks**: Fixed seeds and explicit state management in the command center.
- [x] **II. Data Immutability**: No data modification; read-only access to `data/`.
- [x] **III. Risk-Adjusted**: Sharpe Ratio and Max Drawdown mandated as primary visuals in scorecard.
- [x] **IV. Modular Components**: Visualization logic moved to `lib/visualizer.py`; Notebook used only for coordination.
- [x] **V. Experiment Tracking**: Result data logged to `results/` for every run.
- [x] **VI. Standardized Layout**: Adheres to `lib/`, `notebooks/`, and `results/` structure.

## Project Structure

### Documentation (this feature)

```text
specs/004-test-command-center/
├── plan.md              # This file
├── research.md          # Charting library & Widget compatibility
├── data-model.md        # Session and Metric entities
├── quickstart.md        # Usage guide for the Command Center
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
lib/
├── visualizer.py        # [NEW] Plotly-based charting logic
├── reporting.py         # [NO CHANGE]
├── backtester.py        # [NO CHANGE]
└── strategy_factory.py  # [NO CHANGE]

notebooks/
└── Test_Command_Center.ipynb # [NEW] The interactive cockpit

results/
└── [TIMESTAMP]_run.json # [NEW] Experiment capture
```

**Structure Decision**: 
- Logic is split between `lib/visualizer.py` (rendering) and `notebooks/` (interaction). This keeps the code testable and the notebook clean.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Verification Plan

### Automated Tests
- `pytest tests/test_visualizer.py`: Verify that data conversion for Plotly (e.g., merging price and signals) results in correct trace counts.
- `pytest tests/test_reporting.py`: Ensure metrics used in the scorecard are mathematically correct.

### Manual Verification
1. **Interactive Control**: Open the notebook, change the "Mode" from Mock to Real, and click "Run All". Verify the model loads correctly.
2. **Chart Zoom**: Zoom into a specific drawdown period on the Equity curve and verify markers are visible.
3. **Colab Test**: Upload the directory to Colab, open the notebook, and verify `plotly` widgets render without extra configuration.
