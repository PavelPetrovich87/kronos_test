import argparse
import sys
import torch
import pandas as pd
import os
from lib.data_loader import DataLoader
from lib.strategy import Strategy
from lib.backtester import Backtester
from lib.kronos_model import KronosModel

def create_dummy_data():
    if not os.path.exists("data"):
        os.makedirs("data")
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

def main():
    parser = argparse.ArgumentParser(description="Verify Kronos Strategy")
    parser.add_argument("--mode", choices=["mock", "real"], default="mock", help="Inference mode")
    args = parser.parse_args()

    create_dummy_data()

    # 1. Load Data
    print("Loading data...")
    loader = DataLoader()
    df = loader.load_ohlcv("BTC-USD", "1h")

    # 2. Generate Signals
    print(f"Initializing Strategy (Mode: {args.mode})...")
    
    if args.mode == "real":
        config = {
            "type": "real",
            "model_name": "NeoQuasar/Kronos-small",
            # Auto-detect device for verification script
            "device": "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        }
    else:
        config = {
            "type": "mock",
            "threshold": 0.005
        }
        
    try:
        from lib.strategy_factory import StrategyFactory
        strategy = StrategyFactory.create(config)
        
        # In 'real' mode, the strategy has a KronosModel predictor.
        # In 'mock' mode, it has a MockPredictor.
        # The strategy.generate_signals method abstracts this away.
        # However, for 'real', KronosModel.predict() expects to be called?
        # Strategy.generate_signals calls self.predictor.predict(df) internally now.
        
        signals = strategy.generate_signals(df)
        print(f"Generated {len(signals)} signals.")
        
        if args.mode == "real":
             print("Real model inference check complete.")
             # For real model, we might stop here if we don't want to run full backtest 
             # on just one future prediction.
             return

        # 3. Run Backtest (Mock only for now, or if Real produced valid signals aligned with history)
        backtester = Backtester(initial_capital=10000, fee_pct=0.001)
        result = backtester.run(df, signals)

        # 4. View Results
        print(result.metrics)
        print("Quickstart verification passed.")
        
    except Exception as e:
        print(f"Execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
