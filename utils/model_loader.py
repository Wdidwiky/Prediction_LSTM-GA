from keras.models import load_model
import joblib
from config import Config

print("[DEBUG MODEL PATH]",Config.MODEL_PATH)
try:
    MODEL = load_model(Config.MODEL_PATH)
except:
    MODEL = load_model("model\lstm_ga_brent.keras")

SCALER = joblib.load(Config.SCALER_PATH)