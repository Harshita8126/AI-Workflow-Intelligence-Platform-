import os
import pandas as pd
from app.utils.config import DATA_PROCESSED
from app.ml.predictor import predict_employee_attrition

def get_attrition_risk_distribution():
    path = os.path.join(DATA_PROCESSED, "employee_intelligence_master.csv")
    df = pd.read_csv(path)
    return df['attrition_risk_level'].value_counts().to_dict()

def get_attrition_by_department():
    path = os.path.join(DATA_PROCESSED, "employee_intelligence_master.csv")
    df = pd.read_csv(path)
    dept_risk = df.groupby(['department', 'attrition_risk_level']).size().unstack(fill_value=0).reset_index()
    return dept_risk.to_dict(orient='records')
