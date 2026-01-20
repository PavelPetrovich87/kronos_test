# kronos_test Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-14

## Active Technologies
- Python 3.11 + `pandas` (DataFrames), `numpy` (calculations), `yfinance` (data source - already integrated), `kronos_model` (internal model - stubbed or real). (002-strategy-implementation)
- CSV/Parquet for backtest results and trade logs (in `results/` folder per Constitution). (002-strategy-implementation)
- Python 3.11 + `torch`, `transformers`, `pandas`, `numpy`. (003-model-integration)
- N/A (Read-only model weights). (003-model-integration)
- Python 3.11 + `pandas`, `numpy`, `plotly` (interactive charts), `ipywidgets` (parametric controls), `lib.kronos_model`, `lib.backtester`. (004-test-command-center)
- Reading from `data/*.csv`, logging results to `results/*.json`. (004-test-command-center)

- Python 3.x + `yfinance` (new), `pandas` (existing) (001-yfinance-integration)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.x: Follow standard conventions

## Recent Changes
- 004-test-command-center: Added Python 3.11 + `pandas`, `numpy`, `plotly` (interactive charts), `ipywidgets` (parametric controls), `lib.kronos_model`, `lib.backtester`.
- 003-model-integration: Added Python 3.11 + `torch`, `transformers`, `pandas`, `numpy`.
- 003-model-integration: Added Python 3.11 + `torch`, `transformers`, `pandas`, `numpy`.


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
