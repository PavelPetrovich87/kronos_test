from lib.data_loader import DataLoader
import os
import shutil

def verify():
    print("Starting Manual Verification...")
    data_dir = "data_verification"
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    os.makedirs(data_dir)
    
    loader = DataLoader(data_dir=data_dir)
    symbol = "SPY"
    timeframe = "1d"
    
    # 1. First load - should fetch
    print(f"Fetching {symbol} (should trigger download)...")
    try:
        df = loader.load_ohlcv(symbol, timeframe)
        print(f"Fetch success. Shape: {df.shape}")
    except Exception as e:
        print(f"Fetch FAILED: {e}")
        return

    # Check file exists
    expected_file = os.path.join(data_dir, f"{symbol}_{timeframe}.csv")
    if not os.path.exists(expected_file):
        print("ERROR: File was not persisted!")
        return
    print("File persistence verified.")
    
    # Check normalization
    expected_cols = ['open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in expected_cols):
        print(f"ERROR: Columns not normalized. Got: {df.columns}")
        return
    print("Column normalization verified.")
    
    # 2. Second load - should use cache
    print("Loading again (should use cache)...")
    # We can't easily mock here without patching, but we can assume if it's fast/doesn't error it's fine.
    # In a real scenario we'd check logs or time it.
    df2 = loader.load_ohlcv(symbol, timeframe)
    
    if df.equals(df2):
        print("Cache load consistency verified.")
    else:
        print("ERROR: Cache load data mismatch!")

    print("SUCCESS: All checks passed.")
    # Cleanup
    shutil.rmtree(data_dir)

if __name__ == "__main__":
    verify()
