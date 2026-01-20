import pytest
import pandas as pd
from lib.visualizer import Visualizer
from lib.strategy import Signal, BacktestResult, SignalSide

@pytest.fixture
def mock_backtest_result():
    dates = pd.date_range("2024-01-01", periods=100, freq="h")
    equity = pd.Series([10000 * (1.001 ** i) for i in range(100)], index=dates)
    return BacktestResult(equity_curve=equity, trades=[], metrics={}, config={})

def test_plot_equity_curve_trace_count(mock_backtest_result):
    """Verify figure has the strategy trace."""
    viz = Visualizer()
    fig = viz.plot_equity_curve(mock_backtest_result)
    assert len(fig.data) >= 1
    assert fig.data[0].name == "Strategy"

def test_plot_signals_marker_count():
    """Verify signals are correctly mapped to traces."""
    dates = pd.date_range("2024-01-01", periods=100, freq="h")
    df = pd.DataFrame({"close": [100] * 100}, index=dates)
    signals = [Signal(timestamp=dates[10], symbol="BTC-USD", side=SignalSide.LONG, strength=0.8)]
    
    viz = Visualizer()
    fig = viz.plot_signals(df, signals)
    # Price + Buy marker traces
    assert len(fig.data) >= 2
