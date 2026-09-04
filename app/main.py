from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import joblib
import uuid
import time
from app.models.state import ml_models,model_metadata
from app.logging_config import logger 
from app.routers.v1 import router as v1_router
import json
from app.config import settings
from app.routers.v2 import router as v2_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    ml_models["pipeline"] = joblib.load(settings.MODEL_PATH)

    with open(settings.MODEL_METADATA_PATH) as f:
        
        model_metadata.update(json.load(f)) 

    logger.info("Model loaded successfully")
    
    yield
    
    ml_models.clear()


app = FastAPI(title=settings.API_TITLE, lifespan=lifespan)
app.include_router(v1_router) 
app.include_router(v2_router)


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
    
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(f"request_id={request_id} ValueError caught: {exception}")
    
    return JSONResponse(status_code=500,content={"detail": "Internal error or server error occur while processing the prediction"},)


@app.get("/")
def root():
    
    return {"message": "ML API is alive"}

