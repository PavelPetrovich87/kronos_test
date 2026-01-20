# Data Model: Test Command Center

## Entities

### `BacktestConfig`
A dictionary or TypedDict defining the experimental parameters.
- `symbol` (str): e.g., "BTC-USD"
- `start_date` (datetime): Start of training/validation window.
- `end_date` (datetime): End of window.
- `initial_capital` (float): Seed money.
- `mode` (str): "real" | "mock".
- `threshold` (float): Signal generation threshold.
- `fee_pct` (float): Transaction cost per trade.

### `MetricScorecard`
The key outcomes displayed in the Command Center Table.
- `Total Return (%)`: Cumulative PnL.
- `Sharpe Ratio`: Risk-adjusted return.
- `Max Drawdown (%)`: Peak-to-trough decline.
- `Trade Count`: Total number of long/short entries.
- `Win Rate`: Percentage of profitable trades.

### `ExperimentResult` (Persistence)
The structure of the log file in `results/`.
- `id` (uuid): Unique run identifier.
- `config`: (nested `BacktestConfig`)
- `metrics`: (nested `MetricScorecard`)
- `performance_data`: Link to parity parquet file or embedded snippet of cumulative returns.

## Data Flow
1. **Input Interface**: User sets values in `ipywidgets`.
2. **Execution Engine**: `StrategyFactory` and `Backtester` process the config.
3. **Visual Conversion**: `visualizer.py` converts `BacktestResult` (from `lib/backtester.py`) into Plotly Figures.
4. **Persistence**: Summary is JSON-serialized to `results/`.
