import pandas as pd
import numpy as np

from extensions import cache
from config import Config
from utils.data_loader import load_history
from utils.model_loader import get_model, get_scaler
from utils.preprocessing import create_dataset


def predict():

    df = load_history()
    close = df[["Close"]].copy()

    close = pd.DataFrame(close)
    close.columns = ["Close"]

    scaler = get_scaler()
    model = get_model()

    scaled = scaler.transform(close.to_numpy())
    time_step = Config.TIME_STEP
    X = create_dataset(scaled, time_step)
    pred = model.predict(X, verbose=0)
    pred = scaler.inverse_transform(pred)
    result = close.iloc[time_step:].copy()
    result["Prediction"] = pred
    result["Date"] = result.index
    return result
