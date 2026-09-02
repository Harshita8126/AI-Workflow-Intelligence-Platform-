import os
import pandas as pd
from app.utils.config import DATA_PROCESSED

def get_organization_skill_gaps():
    path = os.path.join(DATA_PROCESSED, "organization_skill_gaps.csv")
    df = pd.read_csv(path)
    return df.head(25).to_dict(orient='records')

def get_all_employees(limit: int = 100):
    path = os.path.join(DATA_PROCESSED, "employee_intelligence_master.csv")
    df = pd.read_csv(path)
    return df.head(limit).to_dict(orient='records')

def get_employee_by_id(emp_id: int):
    master_path = os.path.join(DATA_PROCESSED, "employee_intelligence_master.csv")
    skills_path = os.path.join(DATA_PROCESSED, "employee_skills_controlled.csv")
    
    df_master = pd.read_csv(master_path)
    emp_record = df_master[df_master['employee_id'] == emp_id]
    
    if emp_record.empty:
        return None
        
    record = emp_record.iloc[0].to_dict()
    
    df_skills = pd.read_csv(skills_path)
    current_skills = df_skills[df_skills['employee_id'] == emp_id]['skill_name'].tolist()
    missing_skills = record.get('missing_skills', '').split('|') if pd.notnull(record.get('missing_skills')) and record.get('missing_skills') else []
    
    return {
        "employee_id": int(record['employee_id']),
        "department": record['department'],
        "job_role": record['job_role'],
        "monthly_income": int(record['monthly_income']),
        "years_at_company": int(record['years_at_company']),
        "attrition_probability": float(record['attrition_probability']),
        "attrition_risk_level": record['attrition_risk_level'],
        "engagement_score": float(record['engagement_score']),
        "current_skills_count": int(record['current_skills_count']),
        "missing_skills_count": int(record['missing_skills_count']),
        "career_readiness_pct": float(record['career_readiness_pct']),
        "current_skills": current_skills,
        "missing_skills": missing_skills,
        "recommended_learning_plan": str(record.get('recommended_learning_plan', ''))
    }
