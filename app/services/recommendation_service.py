import os
import pandas as pd
from app.utils.config import DATA_PROCESSED

def get_course_catalog():
    path = os.path.join(DATA_PROCESSED, "course_catalog.csv")
    df = pd.read_csv(path)
    return df.to_dict(orient='records')

def get_upskilling_recommendations():
    path = os.path.join(DATA_PROCESSED, "employee_intelligence_master.csv")
    df = pd.read_csv(path)
    recs = df[['employee_id', 'department', 'job_role', 'career_readiness_pct', 'recommended_learning_plan']].head(50)
    return recs.to_dict(orient='records')
