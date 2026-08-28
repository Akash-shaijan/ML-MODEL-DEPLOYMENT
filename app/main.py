from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import joblib
import uuid
import time
from app.models.schemas import PredictionInput, PredictionOutput
from app.logging_config import logger

ml_models = {}

species_names = ["setosa", "versicolor", "virginica"]

model_version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):

    ml_models["pipeline"] = joblib.load("ml/saved_model/model.joblib")

    logger.info("Model loaded successfully")

    yield

    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):

    request_id = str(uuid.uuid4())
    
    request.state.request_id = request_id

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        
        f"request_id={request_id} method={request.method} "
        
        f"path={request.url.path} duration={duration:.4f}s "
        
        f"status={response.status_code}"
    )

    return response


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exception: ValueError):

    request_id = getattr(request.state, "request_id", "unknown") # to avoid crashing if the request id is empty

    logger.error(f"request_id={request_id} ValueError caught: {exception}")

    return JSONResponse(status_code=500,content={"detail": "Internal error or server error occur while processing the prediction"},)


@app.get("/")
def root():

    return {"message": "ML API is alive"}


@app.get("/health")
def health():

    model_loaded = "pipeline" in ml_models

    return {"status": "ok", "model_loaded": model_loaded}


@app.post("/predict", response_model=PredictionOutput)

def predict(data: PredictionInput, request: Request):

    request_id = request.state.request_id

    features = [[

        data.sepal_length,
        
        data.sepal_width,
        
        data.petal_length,
        
        data.petal_width,

    ]]

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
    
    