from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.validation.employee_schema import EmployeeDetailResponse
from app.services.skill_gap_service import (
    get_organization_skill_gaps, get_all_employees, get_employee_by_id
)
from app.services.recommendation_service import get_upskilling_recommendations, get_course_catalog

router = APIRouter(tags=["Skills & Employees"])

@router.get("/dashboard/skill-gaps")
def skill_gaps():
    return get_organization_skill_gaps()

@router.get("/dashboard/recommendations")
def recommendations():
    return get_upskilling_recommendations()

@router.get("/courses")
def courses():
    return get_course_catalog()

@router.get("/employees")
def list_employees(limit: int = Query(default=100, le=1500)):
    return get_all_employees(limit=limit)

@router.get("/employees/{employee_id}", response_model=EmployeeDetailResponse)
def get_employee(employee_id: int):
    record = get_employee_by_id(employee_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Employee ID {employee_id} not found")
    return record
