# ML Model Deployment as a Monitored REST API

# Overview

This project takes a trained ML model and turns it into a REST API that
other programs can call over the internet, with input validation and
monitoring — instead of just running predictions inside a notebook.

# Dataset & Problem

Using scikit-learn's built-in Iris dataset (load_iris()). The model will
classify a flower into one of three species (setosa, versicolor, virginica)
based on four measurements: sepal length, sepal width, petal length, petal width.

# API Contract

Send the /predict endpoint four measurements from an iris flower —
sepal length, sepal width, petal length, and petal width — and it will
tell you which of the three species (setosa, versicolor, or virginica)
the flower is most likely to be, plus a confidence score indicating how
certain the model is.

In technical terms: the endpoint accepts a POST request containing four
numeric fields (sepal_length, sepal_width, petal_length,
petal_width), and responds with the predicted species and its
associated confidence score.

# Request Flow

1. Client sends a POST request to /predict with the 4 measurements 

2. Pydantic validates that all fields are present and are the correct type

3. If invalid, FastAPI automatically returns a 422 error and the model never runs

4. If valid, the pre-loaded model runs model.predict() to get the species,
   and model.predict_proba() to get the confidence score

5. The API returns the prediction and confidence as a JSON response

# Tech Stack (planned)

Python 3.11+, FastAPI, Pydantic, Uvicorn, scikit-learn, pytest, Docker, Prometheus



# Versioning Plan — How v2 Would Differ From v1

The current API is versioned under '/api/v1/...' using a dedicated `APIRouter',
keeping v1's routes and schemas completely isolated from any future changes.

If a '/api/v2/predict' endpoint were needed tomorrow — for example, to return
an extra field like a full per-class probability breakdown instead of just a
single confidence score — it would be built as follows:

- A new 'PredictionOutputV2' schema would be added to 'schemas.py', containing
  the extra field, without touching the existing 'PredictionOutput' schema.
- A new router file, 'app/routers/v2.py', would be created with its own
  'APIRouter(prefix="/api/v2")', containing the new '/predict' logic.
- The existing v1 router and schema would never be modified directly.

This matters because any client still calling '/api/v1/predict' is relying on 
its exact current response shape. Changing that shape — even by just adding a
field — could silently break their integration. Versioning exists specifically
so breaking changes go into a new version, while old clients keep working
against the version they were built for, untouched. 