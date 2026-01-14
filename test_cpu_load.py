import pandas as pd
import numpy as np
import time
import psutil
import os
from lib.kronos_model import KronosModel

def generate_dummy_data(length=500):
    """Generate random OHLCV data."""
    dates = pd.date_range(start='2024-01-01', periods=length, freq='1h')
    data = {
        'timestamps': dates,
        'open': np.random.rand(length) * 100 + 100,
        'high': np.random.rand(length) * 100 + 105,
        'low': np.random.rand(length) * 100 + 95,
        'close': np.random.rand(length) * 100 + 100,
        'volume': np.random.rand(length) * 1000,
        'amount': np.random.rand(length) * 10000
    }
    return pd.DataFrame(data)

def monitor_process(pid):
    p = psutil.Process(pid)
    return p.memory_info().rss / 1024 / 1024  # MB

def main():
    print("=== Starting CPU Load Test ===")
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024
    print(f"Memory before load: {mem_before:.2f} MB")

    start_load = time.time()
    
    # Initialize Model on CPU
    config = {
        "model_name": "NeoQuasar/Kronos-small",
        "device": "cpu",
        "lookback": 400,
        "pred_len": 10
    }
    
    try:
        print("Initializing KronosModel (this triggers model download/load)...")
        model = KronosModel(config)
        
        load_time = time.time() - start_load
        mem_after_load = process.memory_info().rss / 1024 / 1024
        print(f"Model loaded in {load_time:.2f}s")
        print(f"Memory after load: {mem_after_load:.2f} MB (Delta: {mem_after_load - mem_before:.2f} MB)")
        
        # Generate Data
        print("\nGenerating dummy data (500 rows)...")
        df = generate_dummy_data(500)
        
        # Run Inference
        print("Running inference...")
        start_inf = time.time()
        prediction = model.generate_signals(df)
        inf_time = time.time() - start_inf
        
        print(f"Inference completed in {inf_time:.2f}s")
        print(f"Prediction result shape: {prediction.shape}")
        print(f"Latest prediction: {prediction.iloc[-1]}")
        
        print("\n=== Test PASSED ===")
        
    except Exception as e:
        print(f"\n=== Test FAILED: {e} ===")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
