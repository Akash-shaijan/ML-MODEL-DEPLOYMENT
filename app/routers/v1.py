import time
from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import PredictionInput,PredictionOutput,PredictionBatchInput,PredictionBatchOutput,ModelInfo
from app.models.state import ml_models, model_metadata
from app.logging_config import logger
from app.config import settings
from app.services.predictor import run_inference 

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
        prediction,probabilities = run_inference(features)
        
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


@router.post("/predict-batch", response_model=PredictionBatchOutput)
def predict_batch(data: PredictionBatchInput, request: Request):
    
    request_id = request.state.request_id 
    
    if len(data.inputs) > settings.MAX_BATCH_SIZE:
    
        raise HTTPException(status_code=400,detail=f"Batch size cannot exceed {settings.MAX_BATCH_SIZE}")
    
    start_time = time.time()  

    # Build ONE 2D array from ALL rows — this is what makes it efficient
    features = [
        
        [item.sepal_length, item.sepal_width, item.petal_length, item.petal_width]
        
        for item in data.inputs 
    ]

    try:
        
        predictions = ml_models["pipeline"].predict(features)
        
        probabilities = ml_models["pipeline"].predict_proba(features)
        
    except ValueError:
        
        raise
    
    except Exception as error:
        
        logger.error(f"request_id={request_id} Batch prediction error: {error}")
        
        raise HTTPException(status_code=500, detail="Batch prediction failed") from error

    results = [] 
    
    for pred, probs in zip(predictions, probabilities):
        
        results.append({
            
            "prediction": species_names[pred],
            
            "confidence": float(max(probs)),
            
            "request_id": request_id,
            
            "model_version": model_version,
        })

    duration = time.time() - start_time
    
    logger.info(
        
        f"request_id={request_id} batch_size={len(data.inputs)} "
        
        f"duration={duration:.4f}s"
    )

    return {"predictions": results, "count": len(results)}



@router.get("/model-info", response_model=ModelInfo)
def model_info():
    
    logger.info("model-info requested")
    
    return model_metadata

