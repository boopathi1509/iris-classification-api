import joblib

# Load the saved model
model = joblib.load("ml/saved_model/model.joblib")

# Sample Iris flower measurements
sample = [[5.1, 3.5, 1.4, 0.2]]

# Make prediction
prediction = model.predict(sample)

print("Prediction:", prediction)