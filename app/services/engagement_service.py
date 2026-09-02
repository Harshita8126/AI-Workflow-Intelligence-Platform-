import os
import pandas as pd
from app.utils.config import DATA_PROCESSED

def get_department_engagement_summary():
    path = os.path.join(DATA_PROCESSED, "department_engagement_summary.csv")
    df = pd.read_csv(path)
    return df.to_dict(orient='records')
