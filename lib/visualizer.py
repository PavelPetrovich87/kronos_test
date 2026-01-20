import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from lib.strategy import BacktestResult, Signal, SignalSide


@dataclass
class TestSession:
    """Container for a single backtest experiment."""
    config: Dict[str, Any]
    result: BacktestResult
    timestamp: datetime = field(default_factory=datetime.now)

class Visualizer:
    """
    Handles plotting of backtest results and strategy signals.
    """
    def __init__(self, theme: str = "plotly_white"):
        self.theme = theme

    def plot_equity_curve(self, result: BacktestResult) -> go.Figure:
        """Plots strategy equity vs buy and hold."""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=result.equity_curve.index,
            y=result.equity_curve.values,
            mode='lines',
            name='Strategy',
            line=dict(color='RoyalBlue', width=2)
        ))
        
        fig.update_layout(
            title='Equity Curve',
            xaxis_title='Date',
            yaxis_title='Capital ($)',
            template=self.theme,
            hovermode='x unified'
        )
        return fig

    def plot_signals(self, df: pd.DataFrame, signals: List[Signal]) -> go.Figure:
        """Plots price data with signal markers."""
        fig = go.Figure()
        
        # Price Line
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['close'],
            mode='lines',
            name='Price',
            line=dict(color='gray', width=1, dash='dot')
        ))
        
        # Signal Markers
        buy_signals = [s for s in signals if s.side == SignalSide.LONG]
        sell_signals = [s for s in signals if s.side == SignalSide.SHORT]
        
        if buy_signals:
            fig.add_trace(go.Scatter(
                x=[s.timestamp for s in buy_signals],
                y=[df.loc[s.timestamp, 'close'] for s in buy_signals],
                mode='markers',
                name='Buy',
                marker=dict(symbol='triangle-up', size=12, color='green')
            ))
            
        if sell_signals:
            fig.add_trace(go.Scatter(
                x=[s.timestamp for s in sell_signals],
                y=[df.loc[s.timestamp, 'close'] for s in sell_signals],
                mode='markers',
                name='Sell',
                marker=dict(symbol='triangle-down', size=12, color='red')
            ))
            
        fig.update_layout(
            title='Price and Signals',
            xaxis_title='Date',
            yaxis_title='Price',
            template=self.theme,
            hovermode='closest'
        )
        return fig

    def render_scorecard(self, metrics: Dict[str, float]):
        """Renders a performance scorecard table using Pandas Styler."""
        df = pd.DataFrame([metrics]).T
        df.columns = ['Value']
        df.index.name = 'Metric'
        
        # Formatting
        def style_metrics(v):
            if isinstance(v, float):
                return f"{v:.4f}"
            return v

        styler = df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4B0082'), ('color', 'white'), ('font-family', 'Inter')]},
            {'selector': 'td', 'props': [('font-family', 'Inter'), ('padding', '8px')]}
        ]).set_caption("Strategy Performance Scorecard")
        
        display(styler)

    def render_trade_log(self, trades: List[Dict]):
        """Renders a trade log table."""
        if not trades:
            print("No trades executed.")
            return
            
        df = pd.DataFrame(trades)
        styler = df.style.background_gradient(subset=['profit'], cmap='RdYlGn')\
            .set_caption("Detailed Trade Audit Log")
        
        display(styler)
