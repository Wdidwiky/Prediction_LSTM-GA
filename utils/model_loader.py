from functools import lru_cache

import joblib

from config import Config


@lru_cache(maxsize=1)
def get_model():
    if not Config.MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {Config.MODEL_PATH}")

    from tensorflow.keras.models import load_model

    return load_model(Config.MODEL_PATH, compile=False)


@lru_cache(maxsize=1)
def get_scaler():
    if not Config.SCALER_PATH.exists():
        raise FileNotFoundError(f"Scaler file not found: {Config.SCALER_PATH}")

    return joblib.load(Config.SCALER_PATH)
