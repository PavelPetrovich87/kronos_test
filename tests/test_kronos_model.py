import sys
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import torch

# Mock the external 'model' module before importing KronosModel if possible,
# or patch it during tests. Since KronosModel imports inside __init__ (sort of, or inside _load_model),
# we can patch sys.path and the import.

from lib.kronos_model import KronosModel

class TestKronosModel:
    
    @pytest.fixture
    def config(self):
        return {
            "model_name": "test-model",
            "device": "cpu",
            "lookback": 10,
            "pred_len": 1
        }

    @pytest.fixture
    def mock_kronos_modules(self):
        """Mock the imports from 'model' package"""
        with patch.dict(sys.modules, {'model': MagicMock()}):
             mock_model = sys.modules['model']
             mock_model.Kronos = MagicMock()
             mock_model.KronosTokenizer = MagicMock()
             mock_model.KronosPredictor = MagicMock()
             yield mock_model

    def test_initialization_local(self, config, mock_kronos_modules):
        """Test initialization in Local environment"""
        with patch('lib.kronos_model.sys.path', []) as mock_path:
            with patch('lib.kronos_model.os.path.exists', return_value=True):
                 # KronosModel checks for colab in sys.modules
                 with patch.dict(sys.modules):
                     if 'google.colab' in sys.modules:
                         del sys.modules['google.colab']
                     
                     model = KronosModel(config)
                     
                     # Check if path was added (assuming ../Kronos logic)
                     # The code adds it if not present.
                     assert len(mock_path) > 0
                     assert "Kronos" in mock_path[0]
                     
                     # Verify model loading
                     mock_kronos_modules.Kronos.from_pretrained.assert_called_with("test-model")

    def test_initialization_colab(self, config, mock_kronos_modules):
        """Test initialization in Colab environment"""
        with patch('lib.kronos_model.sys.path', []) as mock_path:
             # Simulate Colab
             with patch.dict(sys.modules, {'google.colab': MagicMock()}):
                 model = KronosModel(config)
                 
                 # Check if path is /content/Kronos
                 assert "/content/Kronos" in mock_path

    def test_predict(self, config, mock_kronos_modules):
        """Test signal generation"""
        with patch.dict(sys.modules, {'model': mock_kronos_modules}):
            model = KronosModel(config)
            
            # Mock predictor output
            mock_predictor = model.predictor
            mock_pred_df = pd.DataFrame({'close': [105.0]})
            mock_predictor.predict.return_value = mock_pred_df
            
            # Create dummy input df
            dates = pd.date_range("2023-01-01", periods=20, freq="1H")
            df = pd.DataFrame({
                "timestamp": dates,
                "open": 100, "high": 101, "low": 99, "close": 100, "volume": 1000
            })
            
            result = model.predict(df)
            
            assert len(result) == 1
            assert result.iloc[0] == 105.0
            # Timestamp should be next hour
            expected_ts = dates[-1] + pd.Timedelta("1H")
            assert result.index[0] == expected_ts

    def test_predict_missing_timestamp(self, config, mock_kronos_modules):
         with patch.dict(sys.modules, {'model': mock_kronos_modules}):
            model = KronosModel(config)
            df = pd.DataFrame({"close": [100]}) # No timestamp
            
            with pytest.raises(ValueError, match="DataFrame must have a 'timestamps' column"):
                model.predict(df)

