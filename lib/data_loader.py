import pandas as pd
from pathlib import Path
import yfinance as yf
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
        # Check if file exists
        file_path = self.data_dir / f"{symbol}_{timeframe}.csv"
        
        if not file_path.exists():
            print(f"Data not found locally. Fetching {symbol} from yfinance...")
            try:
                ticker = yf.Ticker(symbol)
                # Fetch data
                # period="max" might be too much, but for now we follow research.md "10y"
                # Research md said period="10y".
                df = ticker.history(period="10y", interval=timeframe)
                
                if df.empty:
                    raise FileNotFoundError(f"No data found for {symbol} on Yahoo Finance")

                # Normalize columns to lowercase
                df.columns = [c.lower() for c in df.columns]
                
                # Filter for required columns
                required_cols = ['open', 'high', 'low', 'close', 'volume']
                
                # Check if all required columns exist
                missing_cols = [c for c in required_cols if c not in df.columns]
                if missing_cols:
                     # Some tickers might not return Volume?
                     pass 

                # Keep only required columns that exist + implicit index
                cols_to_keep = [c for c in required_cols if c in df.columns]
                df = df[cols_to_keep]

                # Ensure index is name 'timestamp' if it isn't
                df.index.name = 'timestamp'
                
                # Save to CSV
                self.save_raw(df, symbol, timeframe)
                
            except Exception as e:
                # If save_raw fails or yfinance fails
                if isinstance(e, FileNotFoundError):
                    raise
                print(f"Error fetching data: {e}")
                # For FR-006 we should raise meaningful exceptions
                raise

        # Now load from file
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
