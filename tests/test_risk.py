import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from lib.risk import RiskManager

@pytest.fixture
def risk_manager():
    # Threshold 1.0% volatility
    return RiskManager(volatility_threshold=0.01, window=10) # Small window for test

def test_should_trade_low_volatility(risk_manager):
    # Create low vol series (flat)
    prices = pd.Series([100]*20)
    current_time = datetime(2023, 1, 1, 10)
    
    # Should allow trade
    assert risk_manager.can_open_trade(prices, current_time) is True

def test_should_block_trade_high_volatility(risk_manager):
    # Create high vol series (zigzag)
    vals = [100, 105, 95, 105, 95, 105, 95, 105, 95, 105] * 3 
    prices = pd.Series(vals)
    # std of this is approx 5.0 -> 5%. Threshold is 1%.
    
    current_time = datetime(2023, 1, 1, 12) # Just dummy time, assume prices align backward
    
    # But wait, how does RiskManager align prices with time? 
    # Usually we pass the history relevant to the time.
    # For this test, let's assume we pass the series ending at 'current_time'.
    
    assert risk_manager.can_open_trade(prices, current_time) is False
