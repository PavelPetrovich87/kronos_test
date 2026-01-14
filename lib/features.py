import pandas as pd

class FeatureEngineering:
    """
    Stateless feature transformations.
    """
    
    @staticmethod
    def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add technical indicators to the DataFrame.
        Returns a NEW DataFrame (no inplace mutation of original raw data).
        """
        df_features = df.copy()
        
        # Example: Simple Moving Average
        # df_features['sma_20'] = df_features['close'].rolling(window=20).mean()
        
        # Example: RSI
        # ... calculation ...
        
        return df_features

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values, etc.
        """
        return df.dropna()
