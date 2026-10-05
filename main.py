import os
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import joblib
import numpy as np
import requests
from dotenv import load_dotenv

from database import get_db, PredictionLog

load_dotenv()

app = FastAPI(title="Executive Market Value & Compensation Engine")

API_KEY = os.getenv("API_KEY", "my-secret-token-123")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key

# Advanced Request Payload
class MarketAssessmentRequest(BaseModel):
    age: float = Field(..., ge=18, le=80)
    years_experience: float = Field(..., ge=0, le=50)
    current_salary: float = Field(..., ge=0)
    target_role: str = "AI/ML Engineer"
    primary_skill: str = "PyTorch"

def generate_strategic_coaching(role: str, exp: float, predicted: float, current: float, skill: str) -> str:
    token = os.getenv("HF_API_TOKEN")
    gap = predicted - current
    status_str = "underpaid" if gap > 0 else "competitively compensated"
    
    # Standard Fallback logic if API key isn't active
    if not token or token == "your_huggingface_token_here":
        return (
            f"**Market Position**: You are currently {status_str} relative to your target band of ${predicted:,.2f}.\n\n"
            f"**Strategic Priority**: To bridge the gap as a {role} with expertise in {skill}, focus on building production system design portfolios, "
            f"mastering distributed inference optimization, and leading architectural trade-off decisions."
        )

    headers = {"Authorization": f"Bearer {token}"}
    prompt = (
        f"Provide 2 actionable, high-impact career advice points for a {role} with {exp} years of experience specializing in {skill}. "
        f"Their target market value is ${predicted:,.2f} vs current earnings of ${current:,.2f}."
    )
    
    try:
        response = requests.post(
            os.getenv("LLM_API_URL"),
            headers=headers,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 120}},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()[0].get("generated_text", "Advice generated successfully.")
    except Exception as e:
        print(f"LLM Error: {e}")

    return f"Prioritize advanced system architecture and MLOps metrics to command ${predicted:,.2f}."

@app.post("/analyze-market-value", dependencies=[Depends(verify_api_key)])
def analyze_market_value(request: MarketAssessmentRequest, db: Session = Depends(get_db)):
    # Enhanced Market Formula Strategy (Simulating ML weights for YoE + Base Age)
    predicted_salary = round(45000 + (request.years_experience * 8500) + (request.age * 400), 2)
    
    # Calculate Retention/Flight Risk
    delta = predicted_salary - request.current_salary
    if delta > 25000:
        flight_risk = "HIGH (Severely Underpaid)"
    elif delta > 5000:
        flight_risk = "MODERATE (Below Average)"
    else:
        flight_risk = "LOW (Well Retained)"

    # Database Logging
    log_entry = PredictionLog(input_age=request.age, predicted_salary=predicted_salary)
    db.add(log_entry)
    db.commit()

    # AI Executive Coaching Call
    strategy = generate_strategic_coaching(
        request.target_role, 
        request.years_experience, 
        predicted_salary, 
        request.current_salary, 
        request.primary_skill
    )

    return {
        "target_role": request.target_role,
        "current_compensation": f"${request.current_salary:,.2f}",
        "market_valuation": predicted_salary,
        "compensation_delta": round(delta, 2),
        "flight_risk_assessment": flight_risk,
        "executive_ai_strategy": strategy
    }