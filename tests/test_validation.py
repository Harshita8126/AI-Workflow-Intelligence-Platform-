import pytest
from pydantic import ValidationError
from app.validation.employee_schema import AttritionPredictionInput

def test_valid_attrition_input():
    valid_data = {
        "employee_id": 101,
        "age": 35,
        "business_travel": "Travel_Rarely",
        "daily_rate": 800,
        "department": "Research & Development",
        "distance_from_home": 5,
        "education": 3,
        "education_field": "Life Sciences",
        "environment_satisfaction": 3,
        "hourly_rate": 65,
        "job_involvement": 3,
        "job_level": 2,
        "job_role": "Research Scientist",
        "job_satisfaction": 4,
        "monthly_income": 5000,
        "monthly_rate": 15000,
        "num_companies_worked": 2,
        "over_time": "No",
        "percent_salary_hike": 14,
        "performance_rating": 3,
        "relationship_satisfaction": 3,
        "stock_option_level": 1,
        "total_working_years": 10,
        "training_times_last_year": 3,
        "work_life_balance": 3,
        "years_at_company": 5,
        "years_in_current_role": 3,
        "years_since_last_promotion": 1,
        "years_with_curr_manager": 3
    }
    model = AttritionPredictionInput(**valid_data)
    assert model.age == 35
    assert model.monthly_income == 5000

def test_invalid_age_raises_error():
    with pytest.raises(ValidationError):
        AttritionPredictionInput(
            age=15, # Invalid (< 18)
            business_travel="Travel_Rarely",
            daily_rate=800,
            department="Sales",
            distance_from_home=5,
            education=3,
            education_field="Life Sciences",
            environment_satisfaction=3,
            hourly_rate=65,
            job_involvement=3,
            job_level=2,
            job_role="Sales Executive",
            job_satisfaction=3,
            monthly_income=5000,
            monthly_rate=15000,
            num_companies_worked=2,
            over_time="No",
            percent_salary_hike=14,
            performance_rating=3,
            relationship_satisfaction=3,
            stock_option_level=1,
            total_working_years=10,
            training_times_last_year=3,
            work_life_balance=3,
            years_at_company=5,
            years_in_current_role=3,
            years_since_last_promotion=1,
            years_with_curr_manager=3
        )

def test_missing_required_fields_raises_error():
    with pytest.raises(ValidationError):
        AttritionPredictionInput(age=30, department="Sales")
