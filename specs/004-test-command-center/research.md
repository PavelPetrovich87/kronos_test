# Research: Test Command Center

## Decisions & Findings

### Decision 1: Charting Library Selection
- **Chosen**: `Plotly` (`plotly.graph_objects` and `plotly.subplots`)
- **Rationale**: 
    - **Interactivity**: Users need to zoom into specific timestamps to verify signals (P1). 
    - **Colab Compatibility**: `plotly` works out of the box in Colab and Jupyter Lab.
    - **Dual Axis**: Easily handles Price (Primary Y) vs. Signals/Volume (Secondary Y).
- **Alternatives Considered**: 
    - `Matplotlib`: Rejected because static images are difficult to audit for high-frequency signals.
    - `Bokeh`: Rejected due to larger bundle size and more complex server-side requirements.

### Decision 2: Parametric Input Controls
- **Chosen**: `ipywidgets` for interaction, backed by a global `BacktestConfig` dictionary.
- **Rationale**: Standard way to create "app-like" experiences inside notebooks without moving to a full web framework like Streamlit.

### Decision 3: Experiment Tracking
- **Chosen**: JSON-based logging to `results/`.
- **Format**: 
    ```json
    {
      "timestamp": "2026-01-20T19:00:00",
      "config": { "symbol": "BTC-USD", "mode": "real", ... },
      "metrics": { "sharpe": 1.2, "max_dd": 0.15, ... },
      "git_hash": "..."
    }
    ```
- **Rationale**: Adheres to Constitution Principle V. Enables potential future "Leaderboard" of strategy experiments.

## Best Practices
- **Fixed Seeds**: In the Command Center, we must call `np.random.seed()` and `torch.manual_seed()` to ensure the "Real" model produces identical outputs across re-runs.
- **Colab Widget Initialization**: No special tricks needed for modern Colab, but the `lib/visualizer.py` should check for environment if we need to set `plotly` templates (e.g., `plotly_white` for better visibility).

## Unresolved Clarifications
- None. (Informed guesses made: `plotly` is the superior choice for research interactivity).
