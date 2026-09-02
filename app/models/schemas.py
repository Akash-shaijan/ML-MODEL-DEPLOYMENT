from pydantic import BaseModel, Field 

class PredictionInput(BaseModel):
    
    sepal_length: float = Field(..., gt=0, description="Sepal length in cm, must be positive")
    
    sepal_width: float = Field(..., gt=0, description="Sepal width in cm, must be positive")
    
    petal_length: float = Field(..., gt=0, le=10, description="Petal length in cm, must be positive and no more than 10")
    
    petal_width: float = Field(..., gt=0, le=10, description="Petal width in cm, must be positive and no more than 10")
    

class PredictionOutput(BaseModel):
    
    prediction : str
    
    confidence : float
    
    model_version : str
    
    request_id : str
    
    
class PredictionBatchInput(BaseModel):
    
    inputs: list[PredictionInput] = Field(..., min_length=1)


class PredictionBatchOutput(BaseModel):
    
    predictions: list[PredictionOutput]
    
    count: int 


class ModelInfo(BaseModel):
    
    model_type: str
    
    version: str
    
    trained_on: str
    
    features: list[str]  
    
    test_accuracy: float
    
    