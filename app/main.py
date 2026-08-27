from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import joblib
import uuid
from app.models.schemas import PredictionInput, PredictionOutput


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully!")

    yield


app = FastAPI(lifespan=lifespan)

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
def predict(data: PredictionInput):
    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    try:
        
        prediction = app.state.model.predict(features)

        probabilities = app.state.model.predict_proba(features)
        confidence = float(max(probabilities[0]))

        request_id = str(uuid.uuid4())

        return {
            "prediction": int(prediction[0]),
            "confidence": confidence,
            "model_version": "1.0",
            "request_id": request_id
        }

    except Exception as e:
        print(f"Prediction error: {e}")
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