# Testing Report

## Integration Testing

The containerized API was tested using Docker Compose.

### Test Results

| Endpoint                | Result              | Status |
| ----------------------- | ------------------- | ------ |
| `/api/v1/health`        | Passed              | 200    |
| `/api/v1/predict`       | Passed with API key | 200    |
| `/api/v1/predict-batch` | Passed              | 200    |
| `/metrics`              | Passed              | 200    |

The health endpoint confirmed that the ML model was loaded successfully.

The `/metrics` endpoint returned valid Prometheus-format metrics.

The custom ML metric was verified:

`ml_predictions_total{predicted_class="0"} 1.0`

## Load Testing

A basic concurrency test was performed using Python, asyncio, and httpx.

* Concurrent requests: 50
* Successful requests: 50
* Failed requests: 0
* Average response time: 0.7041 seconds
* Total test time: 0.7540 seconds

### Result

All 50 concurrent prediction requests completed successfully with no failures.

## Bug Found and Fixed

### Issue

Docker Compose initially failed to start the API because the Prometheus instrumentation package was not available inside the Docker container.

Error:

`ModuleNotFoundError: No module named 'prometheus_fastapi_instrumentator'`

### Root Cause

The package was installed in the local Python virtual environment but was missing from `requirements.txt`.

### Fix

Added the following dependencies to `requirements.txt`:

```text
prometheus-fastapi-instrumentator==8.1.0
prometheus_client==0.26.0
```

The Docker image was rebuilt successfully and the API started normally.

## Conclusion

Integration testing, load testing, Prometheus metrics verification, and Docker testing were completed successfully.
