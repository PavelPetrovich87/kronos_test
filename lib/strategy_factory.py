from typing import Dict, Any, Union
from lib.strategy import Strategy, MockPredictor
from lib.kronos_model import KronosModel

class StrategyFactory:
    """
    Factory for creating Strategy instances with configured Predictors.
    """
    @staticmethod
    def create(config: Dict[str, Any]) -> Strategy:
        """
        Create a Strategy based on the configuration.
        
        Args:
            config: Dictionary containing 'type' ('real' or 'mock') and other model params.
            
        Returns:
            Strategy instance with the appropriate Predictor.
        """
        mode = config.get('type', 'mock').lower()
        threshold = config.get('threshold', 0.005)
        
        if mode == 'real':
            predictor = KronosModel(config)
        elif mode == 'mock':
            predictor = MockPredictor()
        else:
            raise ValueError(f"Unknown strategy type: {mode}. Use 'real' or 'mock'.")
            
        return Strategy(threshold=threshold, predictor=predictor)
