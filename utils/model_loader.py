from keras.models import load_model
import joblib
from config import Config

MODEL = load_model(Config.MODEL_PATH)
SCALER = joblib.load(Config.SCALER_PATH)