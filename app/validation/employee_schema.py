from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AttritionPredictionInput(BaseModel):
    employee_id: Optional[int] = Field(default=None, description="Employee ID")
    age: int = Field(..., ge=18, le=100, description="Age in years")
    business_travel: str = Field(..., description="Travel_Rarely, Travel_Frequently, Non-Travel")
    daily_rate: int = Field(..., ge=10, description="Daily compensation rate")
    department: str = Field(..., description="Sales, Research & Development, Human Resources")
    distance_from_home: int = Field(..., ge=1, le=100, description="Distance from home in miles")
    education: int = Field(..., ge=1, le=5, description="Education level (1-5)")
    education_field: str = Field(..., description="Education discipline")
    environment_satisfaction: int = Field(..., ge=1, le=4, description="Satisfaction (1-4)")
    hourly_rate: int = Field(..., ge=10, description="Hourly compensation rate")
    job_involvement: int = Field(..., ge=1, le=4, description="Involvement (1-4)")
    job_level: int = Field(..., ge=1, le=5, description="Job level (1-5)")
    job_role: str = Field(..., description="Current job role")
    job_satisfaction: int = Field(..., ge=1, le=4, description="Job satisfaction (1-4)")
    monthly_income: int = Field(..., ge=500, description="Monthly income in USD")
    monthly_rate: int = Field(..., ge=500, description="Monthly rate")
    num_companies_worked: int = Field(..., ge=0, le=20, description="Number of prior companies")
    over_time: str = Field(..., description="Yes or No")
    percent_salary_hike: int = Field(..., ge=0, le=100, description="Percent salary hike")
    performance_rating: int = Field(..., ge=1, le=5, description="Performance rating (1-5)")
    relationship_satisfaction: int = Field(..., ge=1, le=4, description="Relationship satisfaction (1-4)")
    stock_option_level: int = Field(..., ge=0, le=3, description="Stock option level (0-3)")
    total_working_years: int = Field(..., ge=0, le=60, description="Total career years")
    training_times_last_year: int = Field(..., ge=0, le=20, description="Training sessions last year")
    work_life_balance: int = Field(..., ge=1, le=4, description="Work life balance (1-4)")
    years_at_company: int = Field(..., ge=0, le=50, description="Years at current company")
    years_in_current_role: int = Field(..., ge=0, le=40, description="Years in current role")
    years_since_last_promotion: int = Field(..., ge=0, le=30, description="Years since last promotion")
    years_with_curr_manager: int = Field(..., ge=0, le=30, description="Years with current manager")

class AttritionPredictionOutput(BaseModel):
    employee_id: Optional[int]
    attrition_probability: float
    attrition_risk_level: str
    is_at_risk: bool
    model_version: str
    top_contributing_factors: List[Dict[str, Any]]

class DashboardSummaryResponse(BaseModel):
    total_employees: int
    high_risk_employees: int
    medium_risk_employees: int
    low_risk_employees: int
    average_engagement_score: float
    average_readiness_pct: float
    major_skill_gaps_count: int

class EmployeeDetailResponse(BaseModel):
    employee_id: int
    department: str
    job_role: str
    monthly_income: int
    years_at_company: int
    attrition_probability: float
    attrition_risk_level: str
    engagement_score: float
    current_skills_count: int
    missing_skills_count: int
    career_readiness_pct: float
    current_skills: List[str]
    missing_skills: List[str]
    recommended_learning_plan: str

class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="HR Policy question")
    top_k: int = Field(default=3, ge=1, le=10)

class RAGQueryResponse(BaseModel):
    query: str
    answer: str
    retrieved_sources: List[Dict[str, Any]]

class AgentTaskRequest(BaseModel):
    employee_id: int
    target_role: Optional[str] = None
    user_goal: str = Field(..., description="Employee or HR request")

class AgentTaskResponse(BaseModel):
    employee_id: int
    target_role: str
    current_readiness: float
    skill_gap_count: int
    missing_skills: List[str]
    recommended_courses: List[str]
    execution_trace: List[Dict[str, Any]]
    governance_status: str
