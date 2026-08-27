from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib
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

    return {"prediction": int(prediction[0])}