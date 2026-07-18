from functools import lru_cache

import joblib

from config import Config


@lru_cache(maxsize=1)
def get_model():
    if not Config.MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {Config.MODEL_PATH}")

    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense, Dropout, Input, LSTM

    model = Sequential(
        [
            Input(shape=(Config.TIME_STEP, 1), name="lstm_input"),
            LSTM(128, return_sequences=True, name="lstm"),
            Dropout(0.15, name="dropout"),
            LSTM(128, name="lstm_1"),
            Dropout(0.15, name="dropout_1"),
            Dense(1, name="dense"),
        ]
    )
    model.load_weights(Config.MODEL_PATH)
    return model


@lru_cache(maxsize=1)
def get_scaler():
    if not Config.SCALER_PATH.exists():
        raise FileNotFoundError(f"Scaler file not found: {Config.SCALER_PATH}")

    return joblib.load(Config.SCALER_PATH)
