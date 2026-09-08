from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import PredictionInput, PredictionV2Output
from app.logging_config import logger


router = APIRouter(prefix="/api/v2")


@router.post("/predict", response_model=PredictionV2Output)
def predict_v2(data: PredictionInput, request: Request):

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    try:
        model = request.app.state.model

        prediction = model.predict(features)
        probabilities = model.predict_proba(features)

        request_id = request.state.request_id

        probability_distribution = {
            int(class_id): float(probability)
            for class_id, probability in zip(
                model.classes_,
                probabilities[0]
            )
        }

        logger.info(
            f"V2 prediction successful | "
            f"request_id={request_id} | "
            f"prediction={int(prediction[0])}"
        )

        return {
            "prediction": int(prediction[0]),
            "probabilities": probability_distribution,
            "model_version": "1.0",
            "request_id": request_id
        }

    except Exception as e:

        request_id = request.state.request_id

        logger.error(
            f"V2 prediction failed | "
            f"request_id={request_id} | "
            f"error={e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )