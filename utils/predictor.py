import pandas as pd
import numpy as np

from extensions import cache
from config import Config
from utils.data_loader import load_history
from utils.preprocessing import create_dataset

from utils.model_loader import MODEL, SCALER

def predict():

    df = load_history()
    close = df[["Close"]].copy()

    close = pd.DataFrame(close)
    close.columns = ["Close"]

    scaled = SCALER.transform(close.to_numpy())
    time_step = Config.TIME_STEP
    X = create_dataset(scaled, time_step)
    pred = MODEL.predict(X, verbose=0)
    pred = SCALER.inverse_transform(pred)
    result = close.iloc[time_step:].copy()
    result["Prediction"] = pred
    result["Date"] = result.index
    return result
