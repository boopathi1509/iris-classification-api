from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib
import uuid
from app.models.schemas import PredictionInput


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully!")

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "ML API is alive"}


@app.post("/predict")
def predict(data: PredictionInput):
    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = app.state.model.predict(features)

    probabilities = app.state.model.predict_proba(features)
    confidence = float(max(probabilities[0]))

    request_id = str(uuid.uuid4())

    return {
        "prediction": int(prediction[0]),
        "confidence": confidence,
        "request_id": request_id
    }

@app.get("/health")
def health():
    model_loaded = hasattr(app.state, "model")

    return {
        "status": "ok",
        "model_loaded": model_loaded
    }