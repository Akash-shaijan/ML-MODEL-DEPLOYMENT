from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import PredictionInput, PredictionOutputV2
from app.services.predictor import run_inference
from app.logging_config import logger

router = APIRouter(prefix="/api/v2")

species_names = ["setosa", "versicolor", "virginica"]

model_version = "v2"


@router.post("/predict", response_model=PredictionOutputV2)
def predict_v2(data: PredictionInput, request: Request):
    request_id = request.state.request_id

    features = [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]

    try:
        predictions, probabilities = run_inference(features)
    except ValueError:
        raise
    except Exception as error:
        logger.error(f"request_id={request_id} v2 prediction error: {error}")
        raise HTTPException(status_code=500, detail="Prediction failed") from error

    species = species_names[predictions[0]]
    probability_dict = {
        name: float(prob) for name, prob in zip(species_names, probabilities[0])
    }

    logger.info(
        f"request_id={request_id} v2 prediction={species} probabilities={probability_dict}"
    )

    return {
        "prediction": species,
        "probabilities": probability_dict,
        "model_version": model_version,
        "request_id": request_id,
    }