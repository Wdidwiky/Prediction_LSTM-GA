import yfinance as yf
import pandas as pd
from extensions import cache

@cache.cached(timeout=600)
def load_history():
    df=yf.download("BZ=F", period="3y", auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns.name = None
    return df