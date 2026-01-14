import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from lib.data_loader import DataLoader
from pathlib import Path

def test_load_ohlcv_fetches_when_missing(tmp_path):
    """
    Test that load_ohlcv fetches data if it doesn't exist locally.
    """
    loader = DataLoader(data_dir=tmp_path)
    symbol = "ABC"
    timeframe = "1d"
    
    # Mock yfinance
    with patch("lib.data_loader.yf.Ticker") as mock_ticker:
        # Created a mock DataFrame
        mock_df = pd.DataFrame({
            'Open': [100.0],
            'High': [105.0],
            'Low': [99.0],
            'Close': [102.0],
            'Volume': [1000],
            'Dividends': [0.0],
            'Stock Splits': [0.0]
        }, index=pd.to_datetime(['2023-01-01']))
        
        mock_instance = mock_ticker.return_value
        mock_instance.history.return_value = mock_df
        
        # Action
        df = loader.load_ohlcv(symbol, timeframe)
        
        # Assertions
        mock_ticker.assert_called_with(symbol)
        mock_instance.history.assert_called()
        
        # Check columns normalized (part of US2 actually, but basic check here)
        assert 'open' in df.columns
        assert 'close' in df.columns
        assert 'Close' not in df.columns # Normalized
        
        # Check file created
        assert (tmp_path / f"{symbol}_{timeframe}.csv").exists()

def test_load_ohlcv_uses_local_if_exists(tmp_path):
    """
    Test that load_ohlcv uses local file if it exists, avoiding network call.
    """
    loader = DataLoader(data_dir=tmp_path)
    symbol = "XYZ"
    timeframe = "1d"
    
    # Create local file
    file_path = tmp_path / f"{symbol}_{timeframe}.csv"
    df_local = pd.DataFrame({
        'open': [10.0], 'high': [11.0], 'low': [9.0], 'close': [10.5], 'volume': [100]
    })
    df_local.index.name = 'timestamp'
    df_local.to_csv(file_path)
    
    with patch("lib.data_loader.yf.Ticker") as mock_ticker:
        df = loader.load_ohlcv(symbol, timeframe)
        
        mock_ticker.assert_not_called()
        assert not df.empty
        assert len(df) == 1
