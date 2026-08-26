from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    
    sepal_length: float = Field(..., gt=0, description="Sepal length in cm, must be positive")
    
    sepal_width: float = Field(..., gt=0, description="Sepal width in cm, must be positive")
    
    petal_length: float = Field(..., gt=0, description="Petal length in cm, must be positive")
    
    petal_width: float = Field(..., gt=0, le=10, description="Petal width in cm, must be positive and no more than 10") # custum constrain le
    
    