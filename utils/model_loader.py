import joblib
from tensorflow.keras.models import load_model

from config import Config


MODEL = load_model(Config.MODEL_PATH)
SCALER = joblib.load(Config.SCALER_PATH)
