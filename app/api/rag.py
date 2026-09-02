from fastapi import APIRouter, HTTPException
from app.validation.employee_schema import RAGQueryRequest, RAGQueryResponse
from app.services.rag_service import HRPolicyRAGEngine

router = APIRouter(tags=["HR Policy RAG"])

@router.post("/rag/query", response_model=RAGQueryResponse)
def query_hr_policy(payload: RAGQueryRequest):
    try:
        rag = HRPolicyRAGEngine.get_instance()
        result = rag.search(query=payload.query, top_k=payload.top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
