from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib
from app.models.schemas import PredictionInput
import uuid

# This dictionary holds the loaded model so /predict can access it
ml_models = {}

species_names = ["setosa", "versicolor", "virginica"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Runs once, when the server starts
    ml_models["pipeline"] = joblib.load("ml/saved_model/model.joblib")
    
    print("Model loaded successfully")
    
    yield
    
    # Runs once, when the server shuts down
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    
    return {"message": "ML API is alive"}


@app.get("/health")
def health():
    
    model_loaded= "pipeline" in ml_models
    
    return {"status" : "ok", "model_loaded":model_loaded}


@app.post("/predict")
def predict(data: PredictionInput):
    
    features = [[
        
                data.sepal_length,
        
                data.sepal_width,
        
                data.petal_length,
        
                data.petal_width,
                
              ]]
    
    prediction = ml_models["pipeline"].predict(features)
    
    probablities=ml_models["pipeline"].predict_proba(features)
    
    confidence=float(max(probablities[0]))
    
    request_id=str(uuid.uuid4())
    
    species = species_names[prediction[0]]
    
    return {
        
        "prediction": species,
        
        "confidence" : confidence,
        
        "request_id" : request_id
        
        } 

