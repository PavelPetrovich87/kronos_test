import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import pandas as pd
import torch
from lib.strategy import Predictor

class KronosModel(Predictor):
    """
    The Kronos Trading Strategy implementation using the official KronosPredictor.
    Supports Local (Mac/Linux) and Colab environments.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get('model_name', "NeoQuasar/Kronos-small")
        self.tokenizer_name = config.get('tokenizer_name', "NeoQuasar/Kronos-Tokenizer-base")
        # Smart device detection: CUDA > MPS (Mac) > CPU
        if torch.cuda.is_available():
            default_device = "cuda"
        elif torch.backends.mps.is_available():
            default_device = "mps"
        else:
            default_device = "cpu"
        self.device = config.get('device', default_device)
        self.max_context = config.get('max_context', 512)
        
        self._setup_environment()
        self._load_model()
        
    def _is_colab(self) -> bool:
        """Check if running in Google Colab"""
        return 'google.colab' in sys.modules

    def _setup_environment(self):
        """Setup paths to import Kronos repository"""
        # Determine expected Kronos path
        if self._is_colab():
            # In Colab, we expect cloning into /content/Kronos
            kronos_path = Path("/content/Kronos")
        else:
            # Local: Expect sibling directory "../Kronos" relative to this project root
            # This file is in lib/kronos_model.py -> project_root is ../
            project_root = Path(__file__).resolve().parent.parent
            kronos_path = project_root.parent / "Kronos"

        # Allow config override
        if 'kronos_path' in self.config:
            kronos_path = Path(self.config['kronos_path'])
            
        self.kronos_path = kronos_path

        if str(kronos_path) not in sys.path:
            print(f"Adding Kronos path to sys.path: {kronos_path}")
            sys.path.append(str(kronos_path))

    def _load_model(self):
        """Dynamically import and load the model"""
        try:
            # Import here to ensure sys.path is ready
            from model import Kronos, KronosTokenizer, KronosPredictor
            
            print(f"Loading Kronos model: {self.model_name} on {self.device}...")
            self.tokenizer = KronosTokenizer.from_pretrained(self.tokenizer_name)
            self.model = Kronos.from_pretrained(self.model_name)
            self.model.to(self.device)
            
            self.predictor = KronosPredictor(self.model, self.tokenizer, max_context=self.max_context)
            self.predictor.device = self.device # Ensure predictor uses correct device
            print("Model loaded successfully.")
            
        except ImportError as e:
            raise ImportError(f"Could not import Kronos modules. Ensure Kronos repo is at {self.kronos_path}. Error: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load Kronos model: {e}")

    def predict(self, df: pd.DataFrame) -> pd.Series:
        """
        Apply strategy logic to dataframe using KronosPredictor.
        Returns a Series of predicted close prices indexed by prediction timestamp.
        """
        # Ensure timestamps column exists
        working_df = df.copy()
        if 'timestamp' in working_df.columns and 'timestamps' not in working_df.columns:
             working_df = working_df.rename(columns={'timestamp': 'timestamps'})
             
        if 'timestamps' not in working_df.columns:
            if isinstance(working_df.index, pd.DatetimeIndex):
                working_df = working_df.reset_index()
                working_df = working_df.rename(columns={working_df.columns[0]: 'timestamps'})
                if 'timestamps' not in working_df.columns:
                     working_df['timestamps'] = working_df.index
            else:
                 raise ValueError("DataFrame must have a 'timestamps' column or DatetimeIndex")

        lookback = self.config.get('lookback', 400)
        pred_len = self.config.get('pred_len', 1)
        
        # Prepare slice for prediction (take last 'lookback' steps)
        if len(working_df) > lookback:
            df_slice = working_df.iloc[-lookback:].copy()
        else:
            df_slice = working_df.copy()
            
        x_timestamp = df_slice['timestamps']
        
        # Generate future timestamps
        last_ts = x_timestamp.iloc[-1]
        freq = pd.infer_freq(x_timestamp) or '1H'
        y_timestamp = pd.date_range(start=last_ts, periods=pred_len + 1, freq=freq)[1:]
        
        try:
            pred_df = self.predictor.predict(
                df=df_slice,
                x_timestamp=x_timestamp,
                y_timestamp=pd.Series(y_timestamp),
                pred_len=pred_len,
                T=self.config.get('temperature', 1.0),
                top_p=self.config.get('top_p', 0.9),
                sample_count=self.config.get('sample_count', 1)
            )
            
            # Extract predicted close
            predicted_close = pred_df['close'].iloc[-1]
            
            return pd.Series(data=[predicted_close], index=[pd.Timestamp(y_timestamp[0])], name='prediction')
            
        except Exception as e:
            print(f"Prediction failed: {e}")
            return pd.Series(dtype=float)
