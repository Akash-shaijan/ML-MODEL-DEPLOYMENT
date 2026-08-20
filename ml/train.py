from sklearn.datasets import load_iris

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

import joblib


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

