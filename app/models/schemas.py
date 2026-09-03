from typing import List
from pydantic import BaseModel, Field


class PredictionInput(BaseModel):

    sepal_length: float = Field(..., gt=0, description="Sepal length must be positive")

    sepal_width: float = Field(..., gt=0, description="Sepal width must be positive")

    petal_length: float = Field(..., gt=0, description="Petal length must be positive")

    petal_width: float = Field(..., gt=0, description="Petal width must be positive")


class PredictionOutput(BaseModel):

    prediction: int

    confidence: float

    model_version: str

    request_id: str


class PredictionBatchInput(BaseModel):

    inputs: List[PredictionInput] = Field(
        ...,
        min_length=1,
        description="List of prediction inputs"
    )


class PredictionBatchOutput(BaseModel):

    predictions: List[PredictionOutput]