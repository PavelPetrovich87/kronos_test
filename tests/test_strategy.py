import pytest
import pandas as pd
from datetime import datetime
from lib.strategy import Strategy, SignalSide

@pytest.fixture
def mock_data():
    dates = pd.date_range(start='2023-01-01', periods=5, freq='h')
    df = pd.DataFrame({
        'close': [100.0, 100.0, 100.0, 100.0, 100.0],
        'prediction': [102.0, 98.0, 100.0, 100.1, 99.9]  # +2%, -2%, 0%, +0.1%, -0.1%
    }, index=dates)
    return df

def test_generate_signals_long(mock_data):
    s = Strategy(threshold=0.01) # 1% threshold
    signals = s.generate_signals(mock_data)
    
    # 1st row: 102 vs 100 (+2%) -> LONG
    assert signals[0].side == SignalSide.LONG
    assert signals[0].strength > 0

def test_generate_signals_short(mock_data):
    s = Strategy(threshold=0.01)
    signals = s.generate_signals(mock_data)
    
    # 2nd row: 98 vs 100 (-2%) -> SHORT
    assert signals[1].side == SignalSide.SHORT

def test_generate_signals_neutral(mock_data):
    s = Strategy(threshold=0.01)
    signals = s.generate_signals(mock_data)
    
    # 3rd row: 100 vs 100 (0%) -> NEUTRAL
    # 4th row: 100.1 vs 100 (+0.1%) < 1% -> NEUTRAL
    assert signals[2].side == SignalSide.NEUTRAL
    assert signals[3].side == SignalSide.NEUTRAL
