from lib.data_loader import DataLoader
import shutil
from pathlib import Path
import pandas as pd

def main():
    # Setup
    data_dir = Path("data_test_verify")
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir()
    
    loader = DataLoader(data_dir=data_dir)
    symbol = "BTC-USD"
    
    print(f"Fetching {symbol}...")
    try:
        # We need to ensure we don't pick a symbol that fails on yfinance if network is flaky, 
        # but BTC-USD is usually reliable.
        df = loader.load_ohlcv(symbol, timeframe="1d")
        print("Success!")
        print(df.head())
        print("Columns:", df.columns)
        print("Index Name:", df.index.name)
        
        # Verify columns
        expected = ['open', 'high', 'low', 'close', 'volume']
        if not all(c in df.columns for c in expected):
            print(f"FAILED: Missing columns. Got {df.columns}, Expected {expected}")
            exit(1)
            
        # Verify file exists
        if not (data_dir / f"{symbol}_1d.csv").exists():
             print("FAILED: File not saved")
             exit(1)
             
        # Verify loading from file
        print("Loading from file...")
        df2 = loader.load_ohlcv(symbol, timeframe="1d")
        if len(df2) != len(df):
             print(f"FAILED: Length mismatch. Original {len(df)}, Loaded {len(df2)}")
             exit(1)
             
        print("Verification Passed!")
        
    except Exception as e:
        print(f"FAILED: {e}")
        exit(1)
    finally:
        # Cleanup
        if data_dir.exists():
            shutil.rmtree(data_dir)

if __name__ == "__main__":
    main()
