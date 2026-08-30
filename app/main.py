from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import joblib
import uuid
import time
from app.models.schemas import PredictionInput, PredictionOutput
from app.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("ml/saved_model/model.joblib")
    logger.info("ML model loaded successfully")

    yield

logger = setup_logging()

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    try:
        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            f"request_id={request_id} | "
            f"method={request.method} | "
            f"path={request.url.path} | "
            f"status={response.status_code} | "
            f"duration={duration:.4f}s"
        )

        return response

    except Exception as exc:
        duration = time.time() - start_time

        logger.error(
            f"request_id={request_id} | "
            f"method={request.method} | "
            f"path={request.url.path} | "
            f"duration={duration:.4f}s | "
            f"error={exc}"
        )

        raise

class PredictionError(Exception):
    pass


@app.exception_handler(PredictionError)
async def prediction_error_handler(request: Request, exc: PredictionError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Prediction failed"}
    )


@app.get("/")
def root():
    return {"message": "ML API is alive"}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, request: Request):

    request_id = request.state.request_id

    try:
        features = [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]]

        prediction = app.state.model.predict(features)

        probabilities = app.state.model.predict_proba(features)
        confidence = float(max(probabilities[0]))

        logger.info(
            f"Prediction successful | "
            f"request_id={request_id} | "
            f"prediction={int(prediction[0])}"
        )

        return {
            "prediction": int(prediction[0]),
            "confidence": confidence,
            "model_version": "1.0",
            "request_id": request_id
        }

    except Exception as exc:

        logger.error(
            f"Prediction failed | "
            f"request_id={request_id} | "
            f"error={exc}",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

@app.get("/health")
def health():
    model_loaded = hasattr(app.state, "model")

    return {
        "status": "ok",
        "model_loaded": model_loaded
    }