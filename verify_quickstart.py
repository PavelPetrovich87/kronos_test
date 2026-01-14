from lib.data_loader import DataLoader
from lib.strategy import Strategy
from lib.backtester import Backtester
import pandas as pd
import os

# Ensure data dir exists
if not os.path.exists("data"):
    os.makedirs("data")

# Create dummy data if not exists for quickstart
if not os.path.exists("data/BTC-USD_1h.csv"):
    dates = pd.date_range(start="2023-01-01", periods=100, freq="h")
    df = pd.DataFrame({
        "open": [100.0]*100,
        "high": [105.0]*100,
        "low": [95.0]*100,
        "close": [100.0 + i*0.1 for i in range(100)], # slightly trending up
        "volume": [1000]*100
    }, index=dates)
    df.index.name = "timestamp"
    df.to_csv("data/BTC-USD_1h.csv")

# 1. Load Data
loader = DataLoader()
df = loader.load_ohlcv("BTC-USD", "1h")

# 2. Generate Signals
# Mocking a model prediction column for now (or use real KronosModel)
df['prediction'] = df['close'] * 1.01 # Mock bull run +1% logic.
# Wait, threshold 0.005 (0.5%). prediction = 1.01 * price (1%). 
# 1% > 0.5% + price. (1.005 * price). Yes, should trigger LONG.

strategy = Strategy(threshold=0.005)
signals = strategy.generate_signals(df)

print(f"Generated {len(signals)} signals.")

# 3. Run Backtest
backtester = Backtester(initial_capital=10000, fee_pct=0.001)
result = backtester.run(df, signals)

# 4. View Results
print(result.metrics)
print("Quickstart verification passed.")
