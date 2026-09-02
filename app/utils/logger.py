import os
import logging
from datetime import datetime
from app.utils.config import LOGS_DIR, PREDICTIONS_DIR

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(PREDICTIONS_DIR, exist_ok=True)

# Application runtime logger
app_logger = logging.getLogger("EnterpriseHRAI")
app_logger.setLevel(logging.INFO)

if not app_logger.handlers:
    # File handler
    fh = logging.FileHandler(os.path.join(LOGS_DIR, "app.log"), encoding="utf-8")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    fh.setFormatter(formatter)
    app_logger.addHandler(fh)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    app_logger.addHandler(ch)

# Prediction audit logger
pred_logger = logging.getLogger("PredictionAudit")
pred_logger.setLevel(logging.INFO)

if not pred_logger.handlers:
    pfh = logging.FileHandler(os.path.join(PREDICTIONS_DIR, "prediction_audit.log"), encoding="utf-8")
    pfh.setLevel(logging.INFO)
    p_formatter = logging.Formatter('%(asctime)s | %(message)s')
    pfh.setFormatter(p_formatter)
    pred_logger.addHandler(pfh)

def log_prediction(employee_id, model_version, probability, risk_level):
    pred_logger.info(f"EmployeeID={employee_id} | Version={model_version} | Probability={probability:.4f} | Risk={risk_level}")
