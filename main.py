from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# 1. Initialize FastAPI app
app = FastAPI(title="Salary Prediction ML API")

# 2. Load the trained model you generated earlier
model = joblib.load("salary_model.pkl")

# 3. Define input request body structure
class PredictionRequest(BaseModel):
    age: float

# 4. Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Salary Prediction ML API!"}

# 5. Prediction endpoint
@app.post("/predict")
def predict_salary(request: PredictionRequest):
    input_data = np.array([[request.age]])
    prediction = model.predict(input_data)[0]
    return {
        "input_age": request.age,
        "predicted_salary": round(float(prediction), 2)
    }
