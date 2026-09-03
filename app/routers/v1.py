import json
from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import (
    PredictionInput,
    PredictionOutput,
    PredictionBatchInput,
    PredictionBatchOutput
)

from app.logging_config import logger
from app.config import settings


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


@router.post("/predict-batch", response_model=PredictionBatchOutput)
def predict_batch(data: PredictionBatchInput, request: Request):

    if len(data.inputs) > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Batch size cannot exceed {settings.MAX_BATCH_SIZE}"
        )

    features = [
        [
            item.sepal_length,
            item.sepal_width,
            item.petal_length,
            item.petal_width
        ]
        for item in data.inputs
    ]

    try:
        model = request.app.state.model

        predictions = model.predict(features)
        probabilities = model.predict_proba(features)

        request_id = request.state.request_id

        results = []

        for i in range(len(predictions)):

            confidence = float(max(probabilities[i]))

            results.append({
                "prediction": int(predictions[i]),
                "confidence": confidence,
                "model_version": "1.0",
                "request_id": request_id
            })

        logger.info(
            f"Batch prediction successful | "
            f"request_id={request_id} | "
            f"batch_size={len(data.inputs)}"
        )

        return {
            "predictions": results
        }

    except Exception as e:

        request_id = request.state.request_id

        logger.error(
            f"Batch prediction failed | "
            f"request_id={request_id} | "
            f"batch_size={len(data.inputs)} | "
            f"error={e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed"
        )


@router.get("/model-info")
def model_info(request: Request):

    model = request.app.state.model

    with open("ml/saved_model/model_metadata.json", "r") as file:
        metadata = json.load(file)

    metadata["model_type"] = type(model).__name__

    return metadata


# Task 10 - Versioning plan:
# If we create /api/v2/predict later, we can create a separate v2 router
# with a new response schema while keeping /api/v1/predict unchanged.