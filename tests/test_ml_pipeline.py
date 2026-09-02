import pytest
from app.ml.model_loader import ModelRegistry
from app.ml.predictor import predict_employee_attrition

def test_model_registry_load():
    registry = ModelRegistry.get_instance()
    assert registry.pipeline is not None
    assert registry.metadata is not None
    assert "roc_auc" in registry.metadata.get("metrics", {})

def test_predict_attrition_output_bounds():
    sample_payload = {
        "employee_id": 999,
        "age": 42,
        "business_travel": "Travel_Frequently",
        "daily_rate": 600,
        "department": "Sales",
        "distance_from_home": 15,
        "education": 3,
        "education_field": "Marketing",
        "environment_satisfaction": 1,
        "hourly_rate": 55,
        "job_involvement": 2,
        "job_level": 2,
        "job_role": "Sales Executive",
        "job_satisfaction": 1,
        "monthly_income": 3500,
        "monthly_rate": 12000,
        "num_companies_worked": 5,
        "over_time": "Yes",
        "percent_salary_hike": 11,
        "performance_rating": 3,
        "relationship_satisfaction": 2,
        "stock_option_level": 0,
        "total_working_years": 8,
        "training_times_last_year": 1,
        "work_life_balance": 1,
        "years_at_company": 2,
        "years_in_current_role": 1,
        "years_since_last_promotion": 0,
        "years_with_curr_manager": 1
    }
    
    result = predict_employee_attrition(sample_payload)
    assert 0.0 <= result["attrition_probability"] <= 1.0
    assert result["attrition_risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert len(result["top_contributing_factors"]) > 0
