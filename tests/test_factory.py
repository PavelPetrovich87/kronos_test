import pytest
from unittest.mock import MagicMock, patch
from lib.strategy_factory import StrategyFactory
from lib.strategy import Strategy, MockPredictor
from lib.kronos_model import KronosModel

class TestStrategyFactory:
    def test_create_mock_strategy(self):
        """Test creating a MockStrategy"""
        config = {"type": "mock", "threshold": 0.01}
        strategy = StrategyFactory.create(config)
        
        assert isinstance(strategy, Strategy)
        assert isinstance(strategy.predictor, MockPredictor)
        assert strategy.threshold == 0.01

    def test_create_real_strategy(self):
        """Test creating a Real KronosStrategy"""
        config = {"type": "real", "model_name": "test", "device": "cpu"}
        
        # We must mock KronosModel initialization to avoid import errors or heavy lifting
        with patch('lib.strategy_factory.KronosModel') as MockKronos:
            strategy = StrategyFactory.create(config)
            
            assert isinstance(strategy, Strategy)
            assert strategy.predictor == MockKronos.return_value
            MockKronos.assert_called_once_with(config)

    def test_invalid_config(self):
        """Test error handling for invalid configuration"""
        config = {"type": "invalid"}
        with pytest.raises(ValueError, match="Unknown strategy type"):
            StrategyFactory.create(config)
