from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json
from datetime import datetime


data = load_iris()

X, y = data.data, data.target 

# split into train and test

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# created a pipeline

pipeline = Pipeline([
    
                     ("scaler", StandardScaler()),
    
                     ("classifier", RandomForestClassifier(random_state=42)),
    
                     ])


pipeline.fit(X_train, y_train) 

y_pred = pipeline.predict(X_test) 

accuracy = accuracy_score(y_test, y_pred)

print(f"Test accuracy: {accuracy:.4f}")

# save

joblib.dump(pipeline, "ml/saved_model/model.joblib")

print("Model saved to ml/saved_model/model.joblib") 


# model metadata

metadata = {
    
    "model_type": "RandomForestClassifier",
    
    "version": "v1",
    
    "trained_on": datetime.now().isoformat(),
    
    "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
    
    "test_accuracy": accuracy,
           }

with open("ml/saved_model/model_metadata.json", "w") as f:
    
    json.dump(metadata, f, indent=2) 

print("Metadata saved to ml/saved_model/model_metadata.json")

