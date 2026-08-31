from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import PredictionInput, PredictionOutput
from app.models.state import ml_models 
from app.logging_config import logger

router = APIRouter(prefix="/api/v1") 

species_names = ["setosa", "versicolor", "virginica"]

model_version = "v1"

@router.get("/health")
def health():
    
    model_loaded = "pipeline" in ml_models
    
    return {"status": "ok", "model_loaded": model_loaded}


@router.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, request: Request):
    
    request_id = request.state.request_id

    features = [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]

    try:
        
        prediction = ml_models["pipeline"].predict(features)
        
        probabilities = ml_models["pipeline"].predict_proba(features)
        
    except ValueError:
        
        raise
    
    except Exception as error:
        
        logger.error(f"request_id={request_id} Prediction error: {error}")
        
        raise HTTPException(status_code=500, detail="Prediction failed") from error

    confidence = float(max(probabilities[0]))
    
    species = species_names[prediction[0]]

    logger.info(f"request_id={request_id} prediction={species} confidence={confidence:.4f}")

    return {
        
        "prediction": species,
        
        "confidence": confidence,
        
        "request_id": request_id,
        
        "model_version": model_version,
        
    }