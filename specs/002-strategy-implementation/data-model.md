# Data Model: Strategy

## Entities

### `Signal`
Represents the model's output converted into a trading decision.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `datetime` | Time of the signal |
| `symbol` | `str` | Asset (e.g., BTC-USD) |
| `side` | `Enum(LONG, SHORT, NEUTRAL)` | Direction |
| `strength` | `float` | Confidence or raw prediction delta |

### `Trade`
Represents an executed order.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `datetime` | Execution time |
| `symbol` | `str` | Asset |
| `side` | `Enum(LONG, SHORT)` | Direction |
| `price` | `float` | Execution price |
| `quantity` | `float` | Amount traded |
| `cost` | `float` | Transaction fee paid |

### `BacktestResult`
Container for the simulation output.

| Field | Type | Description |
|-------|------|-------------|
| `equity_curve` | `pd.Series` | Account value over time |
| `trades` | `List[Trade]` | Log of all executions |
| `metrics` | `Dict` | {Sharpe, Drawdown, TotalReturn} |
| `config` | `Dict` | Parameters used (thresholds, fees) |
