# Quickstart: Model Integration

## Prerequisites
- `Kronos` repository cloned alongside `kronos_test`.
- `torch` installed.

## Running with Real Model

```python
import sys
from lib.strategy import StrategyFactory
from lib.data_loader import DataLoader

# 1. Configuration
config = {
    "type": "real", # or "mock"
    "model_name": "NeoQuasar/Kronos-small", 
    "device": "cpu" # or "cuda" or "mps"
}

# 2. Initialize Strategy (imports model dynamically)
strategy = StrategyFactory.create(config)

# 3. Load Data
loader = DataLoader()
df = loader.load_ohlcv("BTC-USD", "1h")

# 4. Generate Signals (uses Real Kronos Model)
signals = strategy.generate_signals(df)

print(f"Generated {len(signals)} signals using Real Model.")
```

## Running on Colab

1. **Clone Repos**:
   ```python
   !git clone https://github.com/YourRepo/Kronos.git
   !git clone https://github.com/YourRepo/kronos_test.git
   ```

2. **Install Deps**:
   ```python
   !pip install -r kronos_test/requirements.txt
   ```

4. **Run Verification**:
   ```python
   # In Colab notebook
   import sys
   sys.path.append('/content/kronos_test')
   
   # Run verification script with real model
   !python verify_quickstart.py --mode real
   ```
   
   *Note: Ensure "Runtime type" is set to GPU for faster inference.*
