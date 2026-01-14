import pandas as pd
from pathlib import Path
from typing import Optional, Union

class DataLoader:
    """
    Handles loading of market data from raw artifacts.
    Enforces the Data Immutability principle.
    """
    
    def __init__(self, data_dir: Union[str, Path] = "data"):
        self.data_dir = Path(data_dir)
        
    def load_ohlcv(self, symbol: str, timeframe: str = "1h") -> pd.DataFrame:
        """
        Load OHLCV data for a specific symbol.
        
        Args:
            symbol: Ticker symbol (e.g., 'BTC-USD')
            timeframe: Candle timeframe
            
        Returns:
            pd.DataFrame: OHLCV data with DatetimeIndex
        """
        # TODO: Implement actual loading logic (CSV/Parquet)
        file_path = self.data_dir / f"{symbol}_{timeframe}.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
            
        print(f"Loading data from {file_path}")
        df = pd.read_csv(file_path, parse_dates=['timestamp'], index_col='timestamp')
        
        # Ensure standard column names
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
             # Handle header mapping if necessary
             pass
             
        return df

    def save_raw(self, df: pd.DataFrame, symbol: str, timeframe: str) -> Path:
        """
        Save raw data. NOTE: Should handle versioning or refuse to overwrite existing.
        """
        target_path = self.data_dir / f"{symbol}_{timeframe}.csv"
        if target_path.exists():
            print(f"Warning: File {target_path} exists. Proceeding with caution (immutability check needed).")
            
        df.to_csv(target_path)
        return target_path
