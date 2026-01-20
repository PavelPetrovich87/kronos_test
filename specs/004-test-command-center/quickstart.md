# Quickstart: Test Command Center

The Test Command Center is an interactive research environment designed for strategy backtesting, parametric tuning, and visual verification.

## Prerequisites
- Python 3.11+
- Installed dependencies: `pip install -r requirements.txt`

## Usage Instructions

1.  **Launch Jupyter**: Open `notebooks/Test_Command_Center.ipynb`.
2.  **Configure Cockpit**: 
    - Select your **Symbol** (e.g., `BTC-USD`).
    - Choose **Inference Mode**: `mock` for logic testing, `real` for AI inference.
    - Set the **Signal Threshold** (default: `0.01`).
3.  **Run Backtest**: Click the green "Run Backtest" button.
4.  **Visualize Results**:
    - **Equity Curve**: Zoomable chart showing capital growth.
    - **Signals**: Price overlay with triangle markers (▲ buy, ▼ sell).
    - **Scorecard**: Performance metrics table with Sharpe and Drawdown.
    - **Audit Log**: Sortable table of all executed trades.

## Troubleshooting
- **Interactive Widgets**: If widgets don't appear, ensure `ipywidgets` is enabled in your Jupyter environment.
- **Plotly**: Charts require a modern browser with JavaScript enabled.

> [!TIP]
> **Performance**: The notebook uses the last 500 rows of data by default to ensure interactive performance on local machines.
