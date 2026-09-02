from fastapi import APIRouter, HTTPException
from app.validation.employee_schema import AgentTaskRequest, AgentTaskResponse
from app.services.agent_service import orchestrate_career_upskilling_agent

router = APIRouter(tags=["Governed Agentic AI"])

@router.post("/agent/orchestrate", response_model=AgentTaskResponse)
def run_agent_workflow(payload: AgentTaskRequest):
    try:
        result = orchestrate_career_upskilling_agent(
            employee_id=payload.employee_id,
            target_role=payload.target_role or "",
            user_goal=payload.user_goal
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
