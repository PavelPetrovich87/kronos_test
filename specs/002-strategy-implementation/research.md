# Research: Strategy Implementation

**Status**: Complete
**Decision**: Standard Vectorized Backtesting + Event-Driven Hybrid

## Decisions

### 1. Backtesting Engine Architecture

- **Decision**: Build a custom lightweight backtester in `lib/backtester.py`.
- **Alternatives Considered**:
    - *Backtrader/Lean*: Too heavy, steep learning curve, hard to integrate with our custom `KronosModel`.
    - *VectorBT*: Fast but harder to customize for complex "next-token" logic if we move to transformers.
- **Rationale**: We need full control over the `Signal -> Trade` lifecycle to integrate deeply with `KronosModel` predictions. A custom hybrid approach (vectorized for signals, event-loop for PnL) gives the best balance of speed and control.

### 2. Risk Management Metrics

- **Decision**: Use Annualized Sharpe Ratio and Max Drawdown as primary metrics.
- **Rationale**: Standard industry metrics (Constitution III).
- **Implementation**: `lib/reporting.py` will handle `numpy`-based calculations on the equity curve.

### 3. Signal Generation Logic

- **Decision**: Threshold-based logic.
    - If `prediction > current_price * (1 + threshold)` -> LONG
    - If `prediction < current_price * (1 - threshold)` -> SHORT
    - Else -> NEUTRAL
- **Rationale**: Simple, interpretable, and robust baseline. Can be replaced by ML classifiers later.
