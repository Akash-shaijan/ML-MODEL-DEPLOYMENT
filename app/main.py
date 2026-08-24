from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib

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

@app.post("/predict")
def predict(data: dict = {"sepal_length": 5.1,"sepal_width": 3.5,"petal_length": 1.4,"petal_width": 0.2,}):
    
    features = [[
        
                data["sepal_length"],
        
                data["sepal_width"],
        
                data["petal_length"],
        
                data["petal_width"],
                
              ]]
    
    prediction = ml_models["pipeline"].predict(features)
    
    species = species_names[prediction[0]]
    
    return {"prediction": species}

