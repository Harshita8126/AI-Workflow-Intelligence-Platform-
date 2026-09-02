import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "online"

def test_dashboard_summary():
    res = client.get("/dashboard/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total_employees"] > 0
    assert data["high_risk_employees"] >= 0
    assert 0.0 <= data["average_engagement_score"] <= 100.0

def test_attrition_by_department():
    res = client.get("/dashboard/attrition-by-department")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_skill_gaps_endpoint():
    res = client.get("/dashboard/skill-gaps")
    assert res.status_code == 200
    assert len(res.json()) > 0

def test_recommendations_endpoint():
    res = client.get("/dashboard/recommendations")
    assert res.status_code == 200
    assert len(res.json()) > 0

def test_get_employee_valid():
    res = client.get("/employees/1")
    assert res.status_code == 200
    assert res.json()["employee_id"] == 1

def test_get_employee_not_found():
    res = client.get("/employees/999999")
    assert res.status_code == 404

def test_rag_query_endpoint():
    payload = {"query": "What is the parental leave duration?", "top_k": 3}
    res = client.post("/rag/query", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "parental" in data["answer"].lower() or len(data["retrieved_sources"]) > 0

def test_agent_orchestrate_endpoint():
    payload = {
        "employee_id": 1,
        "target_role": "Sales Executive",
        "user_goal": "Check promotion readiness"
    }
    res = client.post("/agent/orchestrate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["governance_status"] == "AUTHORIZED & COMPLETED"
    assert len(data["execution_trace"]) >= 4
