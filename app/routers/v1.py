from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import PredictionInput, PredictionOutput
from app.logging_config import logger


router = APIRouter(prefix="/api/v1")


@router.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, request: Request):

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    try:
        prediction = request.app.state.model.predict(features)

        probabilities = request.app.state.model.predict_proba(features)
        confidence = float(max(probabilities[0]))

        request_id = request.state.request_id

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

    except Exception as e:
        request_id = request.state.request_id

        logger.error(
            f"Prediction failed | "
            f"request_id={request_id} | "
            f"error={e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )


@router.get("/health")
def health(request: Request):

    model_loaded = hasattr(request.app.state, "model")

    return {
        "status": "ok",
        "model_loaded": model_loaded
    }


# Task 10 - Versioning plan:
# If we create /api/v2/predict later, we can create a separate v2 router
# with a new response schema while keeping /api/v1/predict unchanged.