import pandas as pd
import numpy as np
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class PerformanceMetrics:
    """Calculates risk and performance metrics for backtest results."""

    @staticmethod
    def calculate_sharpe_ratio(equity_curve: pd.Series, risk_free_rate: float = 0.02) -> float:
        """
        Calculates the annualized Sharpe Ratio.
        Assumes hourly data (252 * 24 periods per year approximation).
        """
        returns = equity_curve.pct_change().dropna()
        if returns.std() == 0:
            return 0.0
        
        # Annualized
        excess_returns = returns - (risk_free_rate / (252 * 24))
        sharpe = np.sqrt(252 * 24) * (excess_returns.mean() / returns.std())
        return float(sharpe)

    @staticmethod
    def calculate_max_drawdown(equity_curve: pd.Series) -> float:
        """Calculates the Maximum Drawdown (as a positive percentage)."""
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        max_dd = drawdown.min()
        return float(abs(max_dd))

    @staticmethod
    def calculate_all(equity_curve: pd.Series) -> Dict[str, float]:
        return {
            "sharpe_ratio": PerformanceMetrics.calculate_sharpe_ratio(equity_curve),
            "max_drawdown": PerformanceMetrics.calculate_max_drawdown(equity_curve),
            "total_return": float((equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1) if not equity_curve.empty else 0.0
        }

class ExperimentLogger:
    """Logs experiment results to JSON files."""
    def __init__(self, results_dir: str = "results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def log(self, config: Dict[str, Any], metrics: Dict[str, float]) -> Path:
        """Saves experiment results as a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "metrics": metrics
        }
        
        filename = f"{timestamp}_run.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=4)
        
        return filepath
