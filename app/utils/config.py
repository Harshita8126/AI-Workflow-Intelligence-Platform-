import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_RAW = os.path.join(DATA_DIR, "raw")
DATA_PROCESSED = os.path.join(DATA_DIR, "processed")
DATA_KNOWLEDGE = os.path.join(DATA_DIR, "knowledge")
PREDICTIONS_DIR = os.path.join(DATA_DIR, "predictions")
MODELS_DIR = os.path.join(BASE_DIR, "models")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

MODEL_PATH = os.path.join(MODELS_DIR, "attrition_pipeline.joblib")
METADATA_PATH = os.path.join(MODELS_DIR, "metadata.json")

# Server Config
HOST = "0.0.0.0"
PORT = 8000
