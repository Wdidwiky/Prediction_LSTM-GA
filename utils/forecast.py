import numpy as np
import pandas as pd

from config import Config
from utils.data_loader import load_history
from utils.model_loader import MODEL, SCALER

def forecast_next_days(days=14):
    df = load_history()
    close = df[["Close"]].copy()

    close = pd.DataFrame(close)
    close.columns = ["Close"]

    time_step = Config.TIME_STEP
    scaled = SCALER.transform(close.to_numpy())
    window = scaled[-time_step:]
    forecast = []
    current = window.copy()
    for i in range(days):
        X = current.reshape(1, time_step, 1)
        pred = MODEL.predict(X, verbose=0)
        forecast.append(pred[0][0])
        current = np.vstack((current[1:], pred[0]))

    forecast = np.array(forecast)
    forecast = forecast.reshape(-1, 1)
    forecast = SCALER.inverse_transform(forecast)

    last_date = close.index[-1]
    dates =pd.date_range(last_date + pd.Timedelta(days=1), periods=days)
    
    result = pd.DataFrame({"Date": dates, "Forecast": forecast.flatten()})
    result.attrs["last_price"] = float(close.iloc[-1, 0])
    return result
