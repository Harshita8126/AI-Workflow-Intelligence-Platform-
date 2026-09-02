import pytest
from app.services.skill_gap_service import get_employee_by_id, get_organization_skill_gaps
from app.services.agent_service import tool_calculate_skill_gap, tool_recommend_courses

def test_employee_lookup_valid():
    emp = get_employee_by_id(1)
    assert emp is not None
    assert emp["employee_id"] == 1
    assert "current_skills" in emp
    assert "missing_skills" in emp
    assert 0.0 <= emp["career_readiness_pct"] <= 100.0

def test_employee_lookup_invalid():
    emp = get_employee_by_id(999999)
    assert emp is None

def test_skill_gap_calculation_logic():
    current = ["Python", "SQL", "Pandas"]
    required = ["Python", "SQL", "Docker", "Kubernetes", "MLOps"]
    
    gap = tool_calculate_skill_gap(current, required)
    assert gap["missing_skills"] == ["Docker", "Kubernetes", "MLOps"]
    assert gap["matched_skills"] == ["Python", "SQL"]
    assert gap["readiness_pct"] == 40.0

def test_organization_skill_gaps_not_empty():
    gaps = get_organization_skill_gaps()
    assert len(gaps) > 0
    assert "severity_level" in gaps[0]
