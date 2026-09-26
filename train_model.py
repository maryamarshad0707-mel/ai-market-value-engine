import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# 1. Load the cleaned dataset from Phase 1
df = pd.read_csv("cleaned_data.csv")

# 2. Define Features (X) and Target Variable (y)
X = df[['age']]
y = df['salary']

# 3. Train a Simple Linear Regression Model (Predict Salary based on Age)
model = LinearRegression()
model.fit(X, y)

# 4. Save the trained model to disk
joblib.dump(model, "salary_model.pkl")

print("--- Model Trained and Saved to salary_model.pkl ---")