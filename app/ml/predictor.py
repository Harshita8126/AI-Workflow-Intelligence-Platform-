import pandas as pd
import numpy as np
from app.ml.model_loader import ModelRegistry
from app.utils.logger import app_logger, log_prediction

def predict_employee_attrition(input_dict: dict) -> dict:
    registry = ModelRegistry.get_instance()
    pipeline = registry.pipeline
    metadata = registry.metadata
    version = metadata.get("version", "v1.0.0")
    
    df = pd.DataFrame([input_dict])
    
    # Compute engineered features
    df['over_time_binary'] = (df['over_time'] == 'Yes').astype(int)
    df['tenure_loyalty_ratio'] = np.round(df['years_at_company'] / (df['total_working_years'] + 1), 4)
    df['stagnation_index'] = np.round(df['years_since_last_promotion'] / (df['years_in_current_role'] + 1), 4)
    df['composite_satisfaction'] = np.round(
        (df['job_satisfaction'] + df['environment_satisfaction'] + 
         df['relationship_satisfaction'] + df['job_involvement']) / 4.0, 
        2
    )
    df['income_per_working_year'] = np.round(df['monthly_income'] / (df['total_working_years'] + 1), 2)
    
    # Feature columns expected
    feature_cols = metadata.get("feature_columns", [c for c in df.columns if c != 'employee_id'])
    X = df[feature_cols]
    
    prob = float(pipeline.predict_proba(X)[0, 1])
    
    if prob >= 0.65:
        risk_level = "HIGH"
    elif prob >= 0.35:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
        
    emp_id = input_dict.get('employee_id', 0)
    log_prediction(emp_id, version, prob, risk_level)
    
    # Top contributing explanation factors (rule-based driver identification from inputs)
    factors = []
    if input_dict.get('over_time') == 'Yes':
        factors.append({"factor": "Frequent Overtime Working", "impact": "High Negative Impact (+ Risk)"})
    if input_dict.get('job_satisfaction', 4) <= 2:
        factors.append({"factor": "Low Job Satisfaction Rating", "impact": "Moderate Negative Impact (+ Risk)"})
    if input_dict.get('environment_satisfaction', 4) <= 2:
        factors.append({"factor": "Low Workplace Environment Satisfaction", "impact": "Moderate Negative Impact (+ Risk)"})
    if input_dict.get('years_since_last_promotion', 0) >= 3:
        factors.append({"factor": f"Promotion Stagnation ({input_dict.get('years_since_last_promotion')} yrs without promotion)", "impact": "Moderate Negative Impact (+ Risk)"})
    if input_dict.get('stock_option_level', 1) == 0:
        factors.append({"factor": "Zero Stock Option Incentives", "impact": "Mild Negative Impact (+ Risk)"})
    if not factors:
        factors.append({"factor": "Stable Compensation and High Morale", "impact": "Positive Retention Driver (- Risk)"})

    return {
        "employee_id": emp_id,
        "attrition_probability": round(prob, 4),
        "attrition_risk_level": risk_level,
        "is_at_risk": risk_level in ["MEDIUM", "HIGH"],
        "model_version": version,
        "top_contributing_factors": factors
    }
