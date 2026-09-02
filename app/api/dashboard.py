from fastapi import APIRouter
import pandas as pd
import os
from app.utils.config import DATA_PROCESSED
from app.validation.employee_schema import DashboardSummaryResponse
from app.services.attrition_service import get_attrition_by_department
from app.services.engagement_service import get_department_engagement_summary

router = APIRouter(tags=["Dashboard Analytics"])

@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary():
    master_path = os.path.join(DATA_PROCESSED, "employee_intelligence_master.csv")
    gaps_path = os.path.join(DATA_PROCESSED, "organization_skill_gaps.csv")
    
    df_master = pd.read_csv(master_path)
    df_gaps = pd.read_csv(gaps_path)
    
    total = len(df_master)
    high = int((df_master['attrition_risk_level'] == 'HIGH').sum())
    med = int((df_master['attrition_risk_level'] == 'MEDIUM').sum())
    low = int((df_master['attrition_risk_level'] == 'LOW').sum())
    avg_eng = float(df_master['engagement_score'].mean())
    avg_readiness = float(df_master['career_readiness_pct'].mean())
    major_gaps = int((df_gaps['severity_level'] == 'HIGH').sum())
    
    return {
        "total_employees": total,
        "high_risk_employees": high,
        "medium_risk_employees": med,
        "low_risk_employees": low,
        "average_engagement_score": round(avg_eng, 2),
        "average_readiness_pct": round(avg_readiness, 2),
        "major_skill_gaps_count": major_gaps
    }

@router.get("/dashboard/attrition-by-department")
def attrition_by_department():
    return get_attrition_by_department()

@router.get("/dashboard/engagement-by-department")
def engagement_by_department():
    return get_department_engagement_summary()
