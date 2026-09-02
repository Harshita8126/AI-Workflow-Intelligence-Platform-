from fastapi import APIRouter, HTTPException
from app.validation.employee_schema import AttritionPredictionInput, AttritionPredictionOutput
from app.ml.predictor import predict_employee_attrition

router = APIRouter(tags=["Attrition Prediction"])

@router.post("/predict/attrition", response_model=AttritionPredictionOutput)
def predict_attrition(payload: AttritionPredictionInput):
    try:
        result = predict_employee_attrition(payload.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
