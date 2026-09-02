import os
import json
import joblib
from app.utils.config import MODEL_PATH, METADATA_PATH
from app.utils.logger import app_logger

class ModelRegistry:
    _instance = None
    _pipeline = None
    _metadata = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._load()
        return cls._instance

    def _load(self):
        if not os.path.exists(MODEL_PATH):
            app_logger.error(f"Model file not found at: {MODEL_PATH}")
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        
        self._pipeline = joblib.load(MODEL_PATH)
        app_logger.info(f"Loaded attrition model pipeline from {MODEL_PATH}")
        
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)
            app_logger.info(f"Loaded model metadata version {self._metadata.get('version')}")
        else:
            self._metadata = {"version": "v1.0.0"}

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def metadata(self):
        return self._metadata
