from pathlib import Path


class Config:
    SECRET_KEY = 'brent_prediction'
    BASE_DIR = Path(__file__).resolve().parent
    MODEL_DIR = BASE_DIR / "model"
    MODEL_PATH = MODEL_DIR / "lstm_ga_brent.keras"
    SCALER_PATH = MODEL_DIR /"scaler.pkl"
    TICKER = 'BZ=F'
    START_DATE = "2022-12-30"
    TIME_STEP = 60
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 600
