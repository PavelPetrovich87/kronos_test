import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import torch

# Add the Kronos repository to sys.path to allow importing 'model'
# Assuming Kronos repo is cloned at the project root
KRONOS_REPO_PATH = Path(__file__).resolve().parent.parent / "Kronos"
if str(KRONOS_REPO_PATH) not in sys.path:
    sys.path.append(str(KRONOS_REPO_PATH))

try:
    from model import Kronos, KronosTokenizer, KronosPredictor
except ImportError as e:
    raise ImportError(f"Could not import Kronos modules. Ensure Kronos repo is at {KRONOS_REPO_PATH}. Error: {e}")

# BaseStrategy definition is below.

class BaseStrategy:
    def generate_signals(self, market_data: pd.DataFrame) -> pd.Series:
        raise NotImplementedError

class KronosModel(BaseStrategy):
    """
    The Kronos Trading Strategy implementation using the official KronosPredictor.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get('model_name', "NeoQuasar/Kronos-small")
        self.tokenizer_name = config.get('tokenizer_name', "NeoQuasar/Kronos-Tokenizer-base")
        self.device = config.get('device', "cuda" if torch.cuda.is_available() else "cpu")
        self.max_context = config.get('max_context', 512)
        
        print(f"Loading Kronos model: {self.model_name} on {self.device}...")
        self.tokenizer = KronosTokenizer.from_pretrained(self.tokenizer_name)
        self.model = Kronos.from_pretrained(self.model_name)
        self.model.to(self.device)
        
        self.predictor = KronosPredictor(self.model, self.tokenizer, max_context=self.max_context)
        print("Model loaded successfully.")
        
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """
        Apply strategy logic to dataframe using KronosPredictor.
        
        Args:
            df: DataFrame with at least ['open', 'high', 'low', 'close', 'timestamps']
                'timestamps' column is required by the Predictor.
        
        Returns:
            pd.Series: Forecasted 'close' price (or signal derived from it).
        """
        # Ensure timestamps column exists
        if 'timestamp' in df.columns and 'timestamps' not in df.columns:
             df = df.rename(columns={'timestamp': 'timestamps'})
             
        if 'timestamps' not in df.columns:
            # Fallback for data loader that might set timestamp as index
            if isinstance(df.index, pd.DatetimeIndex):
                df = df.reset_index()
                df = df.rename(columns={df.columns[0]: 'timestamps'}) # Assumption if index name is lost
                if 'timestamps' not in df.columns: # If rename didn't work as expected
                     df['timestamps'] = df.index
            else:
                 raise ValueError("DataFrame must have a 'timestamps' column or DatetimeIndex")

        # Config fields
        lookback = self.config.get('lookback', 400)
        pred_len = self.config.get('pred_len', 1) # Predict next step
        
        # Determine strict range
        # Note: KronosPredictor expects logic:
        # x_df = df.loc[:lookback-1]
        # But we want to run this rolling or for the latest point?
        # For simplicity in this method, let's assume we are predicting AFTER the end of df.
        
        # IMPORTANT: The provided example shows x_timestamp and y_timestamp slicing.
        # We need to adapt this to a standard "Backtest" loop or a "Predict Next" call.
        # If this method is called within a loop, we might need a different signature.
        # For now, let's implement a 'predict_next' style wrapper.
        
        # If DataFrame is long, take the last 'lookback' rows
        if len(df) > lookback:
            df_slice = df.iloc[-lookback:].copy()
        else:
            df_slice = df.copy()
            
        x_timestamp = df_slice['timestamps']
        
        # Generate future timestamps (dummy if just getting value, but model needs strict handling?)
        last_ts = x_timestamp.iloc[-1]
        freq = pd.infer_freq(x_timestamp) or '1H' # Default to 1H if inference fails
        y_timestamp = pd.date_range(start=last_ts, periods=pred_len + 1, freq=freq)[1:]
        
        # Predict
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
            
            # Return prediction. 
            # If we want a Signal, we compare Predicted Close vs Current Close.
            current_close = df_slice['close'].iloc[-1]
            predicted_close = pred_df['close'].iloc[-1]
            
            # Simple Mean Reversion / Trend logic could go here.
            # Returning the raw predicted close for now.
            return pd.Series(data=[predicted_close], index=[pd.Timestamp(y_timestamp[0])]) 
            
        except Exception as e:
            print(f"Prediction failed: {e}")
            return pd.Series(dtype=float)

