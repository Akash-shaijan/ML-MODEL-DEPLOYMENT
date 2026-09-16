# Testing Report

## Integration Testing

Ran `tests/integration/test_integration.py` against the live Docker container started using:

`docker compose up --build`

The tests made real HTTP requests using `httpx` to the following endpoints:

- `/api/v1/health`
- `/api/v1/predict`
- `/api/v1/predict-batch`
- `/metrics`

Result:

`4 passed`

This confirmed that the containerized API worked correctly end-to-end.

---

## Load Testing

Created `scripts/load_test.py` to send concurrent requests to:

`/api/v1/predict`

### 100 Concurrent Requests - Run 1

Total requests       : 100  
Successful requests  : 100  
Failed requests      : 0  
Total test time      : 3.9016 seconds  
Average response time: 3.7642 seconds  
Fastest response     : 3.3653 seconds  
Slowest response     : 3.8410 seconds  

### Single Request Test

Total requests       : 1  
Successful requests  : 1  
Failed requests      : 0  
Total test time      : 0.3577 seconds  
Average response time: 0.3548 seconds  
Fastest response     : 0.3548 seconds  
Slowest response     : 0.3548 seconds  

### 100 Concurrent Requests - Run 2

Total requests       : 100  
Successful requests  : 100  
Failed requests      : 0  
Total test time      : 7.4784 seconds  
Average response time: 7.1309 seconds  
Fastest response     : 5.5696 seconds  
Slowest response     : 7.3601 seconds  

The API handled all requests successfully with no failures.

The tests also showed that response time increased under high concurrent load.

---

## Health Check

After load testing, `/api/v1/health` returned:

`{"status":"ok","model_loaded":true}`

This confirmed that the API and ML model remained healthy after the load test.

---

## Metrics Verification

The `/metrics` endpoint was checked after testing.

Prometheus metrics showed successful HTTP requests and ML predictions.

Example:

`ml_predictions_total{model_version="v1",predicted_class="versicolor"} 101.0`

`ml_predictions_total{model_version="v1",predicted_class="setosa"} 2.0`

This confirmed that successful ML predictions were being recorded in Prometheus metrics.

---

## Issue Found

During testing, the `/api/v1/predict-batch` endpoint was returning predictions correctly, but those predictions were not being counted in the custom Prometheus metric:

`ml_predictions_total`

This meant that the ML monitoring did not include predictions made through the batch endpoint.

---

## Fix Applied

Added the prediction counter inside the batch prediction loop:

```python
species = species_names[pred]

prediction_counter.labels(
    predicted_class=species,
    model_version=model_version
).inc()