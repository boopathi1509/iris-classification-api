from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
import joblib

from app.logging_config import setup_logging, logger
from app.config import settings
from app.routers.v1 import router as v1_router


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load(settings.MODEL_PATH)
    logger.info("ML model loaded successfully")
    yield


app = FastAPI(
    title=settings.API_TITLE,
    lifespan=lifespan
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):

    request_id = str(uuid4())
    request.state.request_id = request_id

    start_time = perf_counter()

    response = await call_next(request)

    duration = perf_counter() - start_time

    logger.info(
        f"request_id={request_id} | "
        f"method={request.method} | "
        f"path={request.url.path} | "
        f"status={response.status_code} | "
        f"duration={duration:.4f}s"
    )

    return response


app.include_router(v1_router)


@app.get("/")
def root():
    return {"message": "ML API is alive"}