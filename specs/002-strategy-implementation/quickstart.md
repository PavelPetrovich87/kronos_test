# Quickstart: Running the Strategy

## Prerequisites
- Data ingested (Phase 2): `data/BTC-USD_1h.csv` must exist.

## Running a Backtest

```python
from lib.data_loader import DataLoader
from lib.strategy import Strategy
from lib.backtester import Backtester

# 1. Load Data
loader = DataLoader()
df = loader.load_ohlcv("BTC-USD", "1h")

# 2. Generate Signals
# Mocking a model prediction column for now (or use real KronosModel)
df['prediction'] = df['close'] * 1.01 # Mock bull run
strategy = Strategy(threshold=0.005)
signals = strategy.generate_signals(df)

# 3. Run Backtest
backtester = Backtester(initial_capital=10000, fee_pct=0.001)
result = backtester.run(df, signals)

# 4. View Results
print(result.metrics)
result.plot() # Requires matplotlib
```

## Running Tests

```bash
pytest tests/test_strategy.py
pytest tests/test_backtester.py
```
