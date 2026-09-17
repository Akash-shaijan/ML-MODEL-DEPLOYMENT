# ML Model Deployment as a Monitored REST API
### Iris Species Classifier

## Overview

This project turns a trained machine learning model into a production-style REST API using FastAPI.

The API accepts Iris flower measurements, validates the input, performs inference using a scikit-learn model, and returns predictions through versioned endpoints.

The project includes:

- Pydantic input validation
- API versioning
- API-key authentication
- Batch prediction
- Structured logging
- Configuration management
- Prometheus monitoring
- Automated testing
- Integration testing
- Load testing
- Docker and Docker Compose
- Continuous integration with GitHub Actions

The goal is to demonstrate the complete process of taking a machine learning model and turning it into a secure, tested, monitored, and containerized API service.

---

## Dataset & Problem

The project uses scikit-learn's built-in Iris dataset with `load_iris()`.

The model classifies a flower into one of three species:

- setosa
- versicolor
- virginica

It uses four input features:

- sepal length
- sepal width
- petal length
- petal width

The trained scikit-learn pipeline is saved using `joblib` and loaded once when the FastAPI application starts.

---

## API Contract

### v1 Prediction Endpoint

`POST /api/v1/predict`

Example request:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Example response:

```json
{
  "prediction": "setosa",
  "confidence": 1.0,
  "request_id": "generated-request-id",
  "model_version": "v1"
}
```

Protected prediction and model-information endpoints require API-key authentication, while public endpoints such as `/api/v1/health` and `/metrics` remain accessible without an API key.

---

## Architecture

```text
Client / Swagger / curl
        ↓
Docker / Uvicorn
        ↓
FastAPI
        ↓
Request Logging Middleware
        ↓
API Key Authentication
        ↓
Pydantic Validation
        ↓
API Router (v1 or v2)
        ↓
Prediction Service (app/services/predictor.py)
        ↓
Scikit-learn Model
        ↓
Prediction Response
        ↓
Structured Logging + Prometheus Metrics
```

The machine learning model is loaded once during application startup through FastAPI's lifespan mechanism and reused for every prediction request.

---

## Request Flow

1. The client sends a request to the API.
2. FastAPI receives the request.
3. A unique request ID is created by the request logging middleware.
4. Protected endpoints verify the `X-API-Key` header.
5. Pydantic validates the input data.
6. Invalid input is rejected before the model is called.
7. Valid input is passed to the prediction service.
8. The pre-loaded scikit-learn model performs inference.
9. The API creates and returns the prediction response.
10. Structured logs and Prometheus metrics are updated.

---

## Tech Stack

- Python 3.13
- FastAPI
- Pydantic
- pydantic-settings
- Uvicorn
- scikit-learn
- joblib
- httpx
- pytest
- Docker
- Docker Compose
- prometheus-client
- prometheus-fastapi-instrumentator
- Git
- GitHub
- GitHub Actions

---

## API Versioning

The project supports two API versions.

### API v1

`POST /api/v1/predict`

Returns:

- prediction
- confidence
- request ID
- model version

### API v2

`POST /api/v2/predict`

Returns:

- prediction
- probability for each species
- request ID
- model version

API versioning allows new response formats to be introduced without breaking clients that still depend on the older v1 response format.

---

## API Endpoints

| Method | Endpoint | Authentication | Purpose |
|---|---|---|---|
| GET | `/` | No | API status |
| GET | `/api/v1/health` | No | Health and model status |
| POST | `/api/v1/predict` | Yes | Single prediction with confidence |
| POST | `/api/v1/predict-batch` | Yes | Batch predictions |
| GET | `/api/v1/model-info` | Yes | Model metadata |
| POST | `/api/v2/predict` | Yes | Prediction with full probabilities |
| GET | `/metrics` | No | Prometheus metrics |
| GET | `/docs` | No | Swagger documentation |

---

## Security and Validation

Protected endpoints require an `X-API-Key` header.

The API key is stored in `.env` and is not committed to Git.

Pydantic validation checks:

- required fields
- numeric data types
- allowed value ranges
- unexpected extra fields

Unexpected fields are rejected using:

```python
extra="forbid"
```

Invalid request data is rejected with HTTP `422` before model inference runs.

Missing or incorrect API keys are rejected with HTTP `401`.

---

## Configuration

Configuration is handled using `pydantic-settings`.

The application reads configuration values from environment variables and `.env`.

Important settings include:

| Variable | Purpose |
|---|---|
| `API_TITLE` | API title shown in Swagger |
| `MODEL_PATH` | Path to the trained model |
| `MODEL_METADATA_PATH` | Path to model metadata |
| `LOG_LEVEL` | Logging level |
| `MAX_BATCH_SIZE` | Maximum allowed batch size |
| `API_KEY` | Secret key for protected endpoints |
| `ALLOWED_ORIGINS` | Allowed CORS origins |

The real `.env` file is ignored by Git.

The `.env.example` file documents the required environment variables without exposing real secret values.

---

## Monitoring and Logging

Prometheus metrics are available at:

```text
/metrics
```

The application exposes automatic HTTP metrics such as:

- request count
- request duration
- request size
- response size

The project also includes a custom machine learning metric:

```text
ml_predictions_total
```

This metric tracks successful predictions using labels for:

- predicted class
- model version

The metric is updated for both single predictions and batch predictions.

Structured logs include information such as:

- request ID
- HTTP method
- request path
- status code
- request duration
- prediction
- confidence
- errors

---

## Testing

The complete test suite can be run with:

```bash
python -m pytest -v
```

Final local test result:

```text
18 passed
```

The test suite includes tests for:

- health endpoint
- model information
- valid predictions
- missing fields
- invalid data types
- negative values
- oversized batches
- missing API keys
- invalid API keys
- extra fields
- API v2
- API version differences
- live integration testing

---

## Integration Testing

Integration tests send real HTTP requests to the running Dockerized API instead of using only an in-process FastAPI test client.

Start the application first:

```bash
docker compose up --build
```

Then run:

```bash
python -m pytest tests/integration/test_integration.py -v
```

Integration test result:

```text
4 passed
```

The integration tests verify:

- health endpoint
- single prediction endpoint
- batch prediction endpoint
- metrics endpoint

---

## Load Testing

A custom asynchronous load test is available at:

```text
scripts/load_test.py
```

Run it using:

```bash
python -m scripts.load_test
```

One 100-request concurrent test produced:

```text
Total requests       : 100
Successful requests  : 100
Failed requests      : 0
Average response time: 3.7642 seconds
```

A second 100-request run also completed with:

```text
Successful requests : 100
Failed requests     : 0
```

The API remained available under concurrent load, although response times increased when many requests were sent at the same time.

More detailed testing information is available in `TESTING.md`.

---

## Issue Found During Testing

During Task 19, the `/api/v1/predict-batch` endpoint returned predictions correctly, but the predictions were not being counted by the custom Prometheus metric.

The batch prediction logic was updated so every successful prediction also increments:

```text
ml_predictions_total
```

This was a monitoring issue rather than a prediction issue.

After the fix, the integration tests were run again successfully.

---

## Running With Docker Compose

### Prerequisites

- Docker Desktop
- Git

Create a `.env` file using `.env.example` as the template and provide a valid API key.

Start the application:

```bash
docker compose up --build
```

The application will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Prometheus metrics:

```text
http://localhost:8000/metrics
```

Start without rebuilding:

```bash
docker compose up
```

Stop the application:

```bash
docker compose down
```

Restart only the API:

```bash
docker compose restart api
```

The trained model directory is bind-mounted into the container:

```yaml
volumes:
  - ./ml/saved_model:/app/ml/saved_model
```

This allows the model files to be updated without rebuilding the entire Docker image.

---

## Local Development Without Docker

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create `.env` using `.env.example`.

Train the model:

```powershell
python ml/train.py
```

Start the FastAPI application:

```powershell
uvicorn app.main:app --reload
```

---

## Example Requests

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### v1 Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

### Batch Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict-batch \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"inputs":[{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}]}'
```

### Model Information

```bash
curl http://localhost:8000/api/v1/model-info \
  -H "X-API-Key: YOUR_API_KEY"
```

### v2 Prediction

```bash
curl -X POST http://localhost:8000/api/v2/predict \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

### Metrics

```bash
curl http://localhost:8000/metrics
```

---

## Deployment

The project is fully reproducible locally using:

```bash
docker compose up --build
```

The Dockerfile is deployment-ready and can be used with a Docker-compatible hosting platform.

A public deployment will be completed as part of the final Task 20 deployment step.

**Public URL:** Pending

---

## Independent Extension: Continuous Integration With GitHub Actions

A GitHub Actions workflow has been prepared at:

```text
.github/workflows/tests.yml
```

The workflow is designed to automatically run the complete pytest suite on every push and pull request to the `main` branch.

The workflow:

1. Checks out the repository.
2. Sets up Python 3.13.
3. Installs project dependencies.
4. Creates a temporary CI environment file.
5. Trains the machine learning model.
6. Builds and starts the application using Docker Compose.
7. Waits until `/api/v1/health` confirms that the API is ready.
8. Runs the complete pytest suite.
9. Stops the Docker containers afterward.

This extension was chosen to automate project testing and help detect problems whenever new code is pushed.

The workflow will be verified after the project is pushed to GitHub.

---

## What I Learned

Building this project helped me understand that machine learning deployment involves much more than simply calling `model.predict()`.

I learned how FastAPI, Pydantic validation, API versioning, API-key authentication, configuration management, structured logging, Prometheus monitoring, pytest, Docker, integration testing, and load testing work together as one complete system.

I also learned the difference between normal automated tests, integration tests, and load tests.

Normal tests helped verify individual API behavior.

Integration tests showed me how to test the real Dockerized application using actual HTTP requests.

Load testing showed me how the application behaves when many requests arrive at the same time.

Another important lesson was understanding how monitoring can expose problems that normal functional testing may not reveal. During testing, the batch prediction endpoint was returning correct predictions, but those predictions were not being included in the Prometheus prediction counter.

Finding and fixing that issue helped me understand why monitoring is an important part of deploying and maintaining machine learning APIs.
