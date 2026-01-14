from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime
from lib.strategy import Signal, SignalSide, Trade, TradeSide, BacktestResult
from lib.reporting import PerformanceMetrics
from lib.risk import RiskManager

class Backtester:
    """
    Simulates trading based on signals and historical data.
    """
    def __init__(self, initial_capital: float = 10000.0, fee_pct: float = 0.001, risk_manager: Optional[RiskManager] = None):
        self.initial_capital = initial_capital
        self.fee_pct = fee_pct
        self.risk_manager = risk_manager

    def run(self, df: pd.DataFrame, signals: List[Signal]) -> BacktestResult:
        """
        Runs the backtest loop.
        
        Args:
            df: OHLCV DataFrame with DatetimeIndex
            signals: List of Signal objects
            
        Returns:
            BacktestResult object
        """
        # Map signals by timestamp for O(1) lookup
        # Assumes at most one signal per timestamp for now
        signal_map = {s.timestamp: s for s in signals}
        
        cash = self.initial_capital
        position = 0.0 # quantity held
        trades: List[Trade] = []
        equity_values = []
        timestamps = []
        
        # Sort dataframe to serve as time axis
        df = df.sort_index()
        
        for timestamp, row in df.iterrows():
            current_price = row['close']
            
            # 1. Execute Trades if Signal exists
            if timestamp in signal_map:
                signal = signal_map[timestamp] # type: ignore
                
                target_position_value = 0.0
                if signal.side == SignalSide.LONG:
                    # Target: 100% Equity in Asset
                    target_position_value = (cash + position * current_price) 
                elif signal.side == SignalSide.SHORT:
                     # Target: -100% Equity? Or just 0 (Cash)?
                     # Warning: Short selling requires margin logic.
                     target_position_value = -1 * (cash + position * current_price)
                elif signal.side == SignalSide.NEUTRAL:
                     target_position_value = 0.0
                
                # Calculate rebalancing trade
                current_position_value = position * current_price
                diff_value = target_position_value - current_position_value
                
                # If diff is substantial
                if abs(diff_value) > 1e-6: # Float epsilon
                    # Risk Management Check
                    allowed = True
                    # Check if we are increasing risk (opening/increasing position)
                    increasing_exposure = abs(target_position_value) > abs(current_position_value)
                    
                    if increasing_exposure and self.risk_manager:
                        # Get history up to now
                        history = df.loc[:timestamp, 'close'] # type: ignore
                        if not self.risk_manager.can_open_trade(history, timestamp): # type: ignore
                            allowed = False
                    
                    if allowed:
                        # Determine quantity
                        qty = diff_value / current_price
                        
                        # Determine Trade Side
                        trade_side = TradeSide.LONG if qty > 0 else TradeSide.SHORT
                        
                        # Transaction Cost
                        trade_value = abs(qty * current_price)
                        cost = trade_value * self.fee_pct
                        
                        # Execute
                        cash -= cost
                        cash -= (qty * current_price) # Buying reduces cash, Selling incr cash
                        position += qty
                        
                        # Log Trade
                        trades.append(Trade(
                            timestamp=timestamp, # type: ignore
                            symbol=signal.symbol,
                            side=trade_side,
                            price=current_price,
                            quantity=abs(qty),
                            cost=cost
                        ))
            
            # 2. Update Equity
            current_equity = cash + (position * current_price)
            equity_values.append(current_equity)
            timestamps.append(timestamp)
            
        equity_curve = pd.Series(equity_values, index=timestamps)
        
        metrics = PerformanceMetrics.calculate_all(equity_curve)
        
        return BacktestResult(
            equity_curve=equity_curve,
            trades=trades,
            metrics=metrics,
            config={"initial_capital": self.initial_capital, "fee_pct": self.fee_pct}
        )
