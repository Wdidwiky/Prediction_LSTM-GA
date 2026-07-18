import tempfile
from pathlib import Path

import yfinance as yf
import pandas as pd
from config import Config
from extensions import cache


FALLBACK_HISTORY_PATH = Config.BASE_DIR / "brent_actual.csv"
YFINANCE_CACHE_DIR = Config.BASE_DIR / ".cache" / "yfinance"


def _configure_yfinance_cache():
    cache_dir = YFINANCE_CACHE_DIR
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        cache_dir = Path(tempfile.gettempdir()) / "brent-yfinance-cache"
        cache_dir.mkdir(parents=True, exist_ok=True)

    if hasattr(yf, "set_tz_cache_location"):
        yf.set_tz_cache_location(str(cache_dir))


def _normalize_history(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns.name = None

    if "Date" in df.columns:
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.set_index("Date")
    else:
        df = df.copy()
        df.index = pd.to_datetime(df.index, errors="coerce")

    if "Close" not in df.columns:
        raise ValueError("History data must contain a Close column")

    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df[df.index.notna()]
    df = df.dropna(subset=["Close"])
    df = df.sort_index()

    if df.empty:
        raise ValueError("History data is empty after normalization")

    if len(df) <= Config.TIME_STEP:
        raise ValueError(
            f"History data must contain more than {Config.TIME_STEP} rows, got {len(df)}"
        )

    return df


def _load_fallback_history():
    if not FALLBACK_HISTORY_PATH.exists():
        raise FileNotFoundError(f"Fallback history file not found: {FALLBACK_HISTORY_PATH}")

    df = pd.read_csv(
        FALLBACK_HISTORY_PATH,
        skiprows=3,
        names=["Date", "Close", "High", "Low", "Open", "Volume"],
    )
    return _normalize_history(df)


@cache.cached(timeout=600)
def load_history():
    try:
        _configure_yfinance_cache()
        df = yf.download(Config.TICKER, period="3y", auto_adjust=True, progress=False)
        return _normalize_history(df)
    except Exception:
        return _load_fallback_history()
