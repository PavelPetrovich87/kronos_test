import pytest
import pandas as pd
from datetime import datetime, timedelta
from lib.strategy import Signal, SignalSide, TradeSide
from lib.backtester import Backtester

@pytest.fixture
def sample_data():
    dates = pd.date_range(start='2023-01-01', periods=10, freq='h')
    df = pd.DataFrame({
        'close': [100, 101, 102, 101, 100, 99, 98, 97, 96, 90]
    }, index=dates)
    return df

@pytest.fixture
def sample_signals(sample_data):
    # Create manual signals:
    # t0: LONG (price 100)
    # t2: NEUTRAL (price 102) -> Should close long
    # t6: SHORT (price 98)
    # t9: NEUTRAL (price 101) -> Should close short
    
    signals = []
    idx = sample_data.index
    
    signals.append(Signal(idx[0], "BTC-USD", SignalSide.LONG))
    signals.append(Signal(idx[2], "BTC-USD", SignalSide.NEUTRAL))
    signals.append(Signal(idx[6], "BTC-USD", SignalSide.SHORT))
    signals.append(Signal(idx[9], "BTC-USD", SignalSide.NEUTRAL))
    
    return signals

def test_backtester_execution_flow(sample_data, sample_signals):
    initial_capital = 10000.0
    fee_pct = 0.001 # 0.1%
    
    backtester = Backtester(initial_capital=initial_capital, fee_pct=fee_pct)
    result = backtester.run(sample_data, sample_signals)
    
    assert hasattr(result, 'equity_curve')
    assert hasattr(result, 'trades')
    assert len(result.trades) >= 2 # Should have at least 2 round trips or 4 trades
    
    # Check 1st trade: Buy at 100 (approx)
    trade1 = result.trades[0]
    assert trade1.side == TradeSide.LONG
    assert trade1.price == 100.0
    
    # Check 2nd trade: Sell at 102 (approx)
    trade2 = result.trades[1]
    assert trade2.side == TradeSide.SHORT # Closing a long is a sell (SHORT side order)
    assert trade2.price == 102.0
    
    # PnL roughly: (102 - 100) * qty - fees
    # Profit ~ 2% minus fees.
    assert result.equity_curve.iloc[-1] > initial_capital # Should be profitable in this scenario

def test_transaction_costs(sample_data):
    # Scenario: Buy and immediately sell at same price -> should lose money due to fees
    dates = sample_data.index
    signals = [
        Signal(dates[0], "BTC-USD", SignalSide.LONG),
        Signal(dates[1], "BTC-USD", SignalSide.NEUTRAL)
    ]
    # Price is 100 -> 101. Wait, 101 is profit. 
    # Let's force prices to be flat
    sample_data['close'] = 100.0
    
    backtester = Backtester(initial_capital=10000, fee_pct=0.01) # 1% fee
    result = backtester.run(sample_data, signals)
    
    final_equity = result.equity_curve.iloc[-1]
    assert final_equity < 10000
