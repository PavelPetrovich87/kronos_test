import pandas as pd
import numpy as np
import time
import psutil
import os
import torch
from lib.kronos_model import KronosModel

def get_best_device():
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

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

def main():
    target_device = get_best_device()
    print(f"=== Starting GPU Load Test on {target_device.upper()} ===")
    
    if target_device == "cpu":
        print("WARNING: No GPU detected (CUDA or MPS). Aborting GPU test.")
        return

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024
    
    start_load = time.time()
    
    # Initialize Model on GPU
    config = {
        "model_name": "NeoQuasar/Kronos-small",
        "device": target_device,
        "lookback": 400,
        "pred_len": 10
    }
    
    try:
        print(f"Initializing KronosModel on {target_device}...")
        model = KronosModel(config)
        
        load_time = time.time() - start_load
        mem_after_load = process.memory_info().rss / 1024 / 1024
        print(f"Model loaded in {load_time:.2f}s")
        print(f"Host Memory usage: {mem_after_load:.2f} MB")
        
        # Generate Data
        df = generate_dummy_data(500)
        
        # Run Inference
        print("Running inference...")
        # Warmup
        _ = model.generate_signals(df)
        
        # Timed Run
        start_inf = time.time()
        prediction = model.generate_signals(df)
        inf_time = time.time() - start_inf
        
        print(f"Inference completed in {inf_time:.2f}s")
        print(f"Prediction result: {prediction.iloc[-1]}")
        
        print("\n=== Test PASSED ===")
        
    except Exception as e:
        print(f"\n=== Test FAILED: {e} ===")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
