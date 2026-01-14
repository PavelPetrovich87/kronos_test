from datetime import datetime
import pandas as pd
import numpy as np

class RiskManager:
    """
    Manages risk controls for the strategy.
    Primary mechanism: Volatility Filter.
    """
    def __init__(self, volatility_threshold: float = 0.02, window: int = 24):
        """
        Args:
            volatility_threshold: Max allowed rolling std dev of returns. (Default 2% per period)
            window: Lookback window for volatility calculation (e.g., 24 hours).
        """
        self.volatility_threshold = volatility_threshold
        self.window = window

    def can_open_trade(self, prices: pd.Series, current_time: datetime = None) -> bool:
        """
        Checks if a trade can be opened based on recent price volatility.
        Args:
            prices: Series of recent close prices. Should encompass at least `window + 1` periods.
            current_time: Optional, unused here but kept for API consistency if accessing full DF.
        """
        if len(prices) < self.window + 1:
            return True # Not enough data to assess risk, assuming safe to start
            
        returns = prices.pct_change()
        # Calculate volatility (std dev of returns)
        # We only need the latest value
        rolling_vol = returns.rolling(window=self.window).std()
        
        current_vol = rolling_vol.iloc[-1]
        
        if pd.isna(current_vol):
            return True
            
        return float(current_vol) <= self.volatility_threshold
