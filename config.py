import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "brent_prediction")
    BASE_DIR = Path(__file__).resolve().parent
    MODEL_DIR = BASE_DIR / "model"
    MODEL_PATH = MODEL_DIR / "lstm_ga_brent.h5"
    SCALER_PATH = MODEL_DIR / "scaler.pkl"
    TICKER = os.environ.get("TICKER", "BZ=F")
    START_DATE = os.environ.get("START_DATE", "2022-12-30")
    TIME_STEP = int(os.environ.get("TIME_STEP", "60"))
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "600"))
