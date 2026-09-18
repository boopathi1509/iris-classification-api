# Iris Flower Classification API

A Machine Learning API that predicts the Iris flower type using **FastAPI** and **Logistic Regression**.

## Features

* Iris flower prediction
* FastAPI REST API
* API validation
* API key security
* API v1 and v2
* Batch prediction
* Docker & Docker Compose
* Prometheus monitoring
* Automated testing

## Technologies

* Python
* FastAPI
* Scikit-learn
* Pandas
* Docker
* Prometheus
* Pytest

## Architecture

text
User
  ↓
FastAPI
  ↓
Validation + API Key
  ↓
ML Model
  ↓
Prediction
  ↓
Response + Logs + Metrics


## How to Run

Make sure Docker Desktop is running.

bash
docker compose up --build


Open Swagger:

text
http://localhost:8000/docs


## API Endpoints

### Health

text
GET /api/v1/health


### Prediction V1

text
POST /api/v1/predict


Example:

bash
curl -X POST http://localhost:8000/api/v1/predict -H "Content-Type: application/json" -H "X-API-Key: your-api-key-here" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"


### Prediction V2

text
POST /api/v2/predict


### Batch Prediction

text
POST /api/v1/predict-batch


### Model Information

text
GET /api/v1/model-info


### Metrics

text
GET /metrics


## Testing

Run:

```bash
pytest -v


Latest result:

`text
11 passed
`

Load test:

`bash
python load_test.py
`

Result:

`text
50 successful
0 failed
`

## Security

Prediction endpoints require an `X-API-Key`.

Invalid or missing API keys return `401 Unauthorized`.

## What I Learned

I learned how to:

* Build an ML model
* Create a FastAPI service
* Validate API inputs
* Add API security
* Use Docker and Docker Compose
* Add Prometheus monitoring
* Write automated tests
* Perform load testing

## Independent Extension

Will be added as part of Task 20.

## Project Status

Core API, testing, Docker, security and monitoring are completed.

Public deployment and independent extension are pending.
