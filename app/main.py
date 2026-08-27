from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model once when the application starts
    app.state.model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully!")

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "ML API is alive"}


@app.post("/predict")
def predict():
    features = [[6.7, 3.0, 5.2, 2.3]]

    prediction = app.state.model.predict(features)

    return {"prediction": int(prediction[0])}