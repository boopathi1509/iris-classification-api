# Iris Flower Classification API

## Project Overview

This project aims to build a simple Machine Learning REST API that predicts the species of an Iris flower based on its measurements.

## Dataset

Iris Dataset from Scikit-learn.

## Machine Learning Problem

Classification

## Machine Learning Model

Logistic Regression

## Iris Flower Species

- Setosa
- Versicolor
- Virginica

## API Contract

The `/predict` endpoint will accept four numerical values representing the measurements of an Iris flower.

The API will validate the input values and send them to the Machine Learning model. The model will predict the species of the Iris flower.

The API will return the predicted flower species in JSON format.

### Input

The API accepts:

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

### Example Input

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}

## How to run this project

1. Make sure Docker Desktop is running.

2. Open PowerShell in the project folder.

3. Run:
   docker compose up --build

4. Open the API documentation:
   http://localhost:8000/docs

5. To stop the application:
   Ctrl + C