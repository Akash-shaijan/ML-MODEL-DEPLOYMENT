# Testing Report

## Integration Testing

`tests/integration/test_integration.py` was run against the live Docker container, started with:

```bash
docker compose up --build
```

The tests make real `httpx` requests against the running API at:

```text
http://localhost:8000
```

The integration tests cover:

- `/api/v1/health`
- `/api/v1/predict`
- `/api/v1/predict-batch`
- `/metrics`

Result:

```text
4 passed
```

This verified that the containerized API works correctly end-to-end, not just through isolated in-process tests.

---

## Full Test Suite

The complete pytest suite was run with:

```bash
python -m pytest -v
```

Final result:

```text
18 passed
```

This confirmed that both the normal automated tests and the live integration tests passed successfully.

---

## Load Testing

A custom asynchronous load test was created at:

```text
scripts/load_test.py
```

It sends concurrent requests to:

```text
/api/v1/predict
```

The script must be run with:

```bash
python -m scripts.load_test
```

Running it directly as:

```bash
python scripts/load_test.py
```

causes an import error because the script imports from `app.config` and needs the project root on the Python import path.

### Single Request Baseline

```text
Total requests       : 1
Successful requests  : 1
Failed requests      : 0
Total test time      : 0.3577 seconds
Average response time: 0.3548 seconds
Fastest response     : 0.3548 seconds
Slowest response     : 0.3548 seconds
```

### 100 Concurrent Requests — Run 1

```text
Total requests       : 100
Successful requests  : 100
Failed requests      : 0
Total test time      : 3.9016 seconds
Average response time: 3.7642 seconds
Fastest response     : 3.3653 seconds
Slowest response     : 3.8410 seconds
```

### 100 Concurrent Requests — Run 2

```text
Total requests       : 100
Successful requests  : 100
Failed requests      : 0
Total test time      : 7.4784 seconds
Average response time: 7.1309 seconds
Fastest response     : 5.5696 seconds
Slowest response     : 7.3601 seconds
```

### Load Test Observation

Across the three load-test runs, all requests completed successfully with zero failures.

However, the average response time under identical 100-concurrent-request conditions increased noticeably between Run 1 and Run 2:

```text
Run 1 average: 3.7642 seconds
Run 2 average: 7.1309 seconds
```

The exact cause of this variation was not confirmed during this testing pass.

Possible factors could include:

- system load
- Docker container resource usage
- operating system scheduling
- request scheduling
- other runtime conditions

A more detailed performance investigation would be required to identify the exact cause.

---

## Health Check

After load testing, the health endpoint was checked:

```text
GET /api/v1/health
```

Response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

This confirmed that the API and machine learning model remained healthy after the load tests.

---

## Metrics Verification

The `/metrics` endpoint was checked after testing.

Prometheus metrics confirmed that successful predictions were being recorded.

Example:

```text
ml_predictions_total{model_version="v1",predicted_class="versicolor"} 101.0
ml_predictions_total{model_version="v1",predicted_class="setosa"} 2.0
```

This showed that successful machine learning predictions were being counted by the custom Prometheus metric.

---

## Issue Found During Testing

During Task 19 testing, the `/api/v1/predict-batch` endpoint was returning predictions correctly to the client.

However, predictions made through the batch endpoint were not being counted by the custom Prometheus metric:

```text
ml_predictions_total
```

Single predictions made through `/api/v1/predict` were counted correctly, but predictions made through `/api/v1/predict-batch` were missing from the monitoring data.

This meant the API prediction logic was working correctly, but the monitoring data was incomplete.

---

## Fix Applied

The missing Prometheus counter increment was added inside the batch prediction loop in:

```text
app/routers/v1.py
```

The fix:

```python
species = species_names[pred]

prediction_counter.labels(
    predicted_class=species,
    model_version=model_version
).inc()
```

Now every prediction inside a batch increments the custom prediction counter individually.

---

## Fix Verification

Before the fix:

```text
/predict-batch
        ↓
predictions returned successfully
        ↓
ml_predictions_total did not increase
```

After the fix:

```text
/predict-batch
        ↓
predictions returned successfully
        ↓
each batch prediction increments ml_predictions_total
```

The fix was verified by checking `/metrics` before and after sending batch prediction requests.

The integration tests were also run again successfully after the change.

---

## Warnings

The final pytest run completed successfully with all 18 tests passing.

Some dependency-related deprecation warnings were shown by packages such as:

- Starlette / httpx
- joblib / NumPy

These warnings did not cause test failures and were not treated as blocking issues for the project.

---

## Conclusion

The final containerized application passed all automated and integration tests successfully.

Final test results:

```text
18 passed
```

Integration result:

```text
4 passed
```

Load testing showed:

```text
100 concurrent requests
100 successful
0 failed
```

The API remained healthy after load testing.

Testing also revealed a genuine monitoring issue where batch predictions were missing from the Prometheus prediction counter. The issue was fixed and verified successfully.

The variation in load-test response times was documented as an unresolved performance observation rather than being treated as a confirmed bug.