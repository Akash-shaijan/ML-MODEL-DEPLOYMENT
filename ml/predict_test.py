import joblib

# load 
pipeline = joblib.load("ml/saved_model/model.joblib") 

# sepal,petal lenght and width 
sample = [[6.3, 3.3, 6.0, 2.5]]

prediction = pipeline.predict(sample) 

species = ["setosa", "versicolor", "virginica"]

print(f"Predicted species: {species[prediction[0]]}")  

