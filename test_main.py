from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

API_KEY = "my-secret-token-123"

def test_unauthorized_access():
    """Ensure requests without an API key are rejected (401)."""
    response = client.post("/analyze-market-value", json={})
    assert response.status_code == 401

def test_analyze_market_value_success():
    """Test full endpoint pipeline with valid payload and auth header."""
    headers = {"X-API-Key": API_KEY}
    payload = {
        "age": 28,
        "years_experience": 5,
        "current_salary": 90000,
        "target_role": "AI/ML Engineer",
        "primary_skill": "PyTorch"
    }
    
    response = client.post("/analyze-market-value", json=payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "market_valuation" in data
    assert "flight_risk_assessment" in data
    assert "executive_ai_strategy" in data
    assert data["market_valuation"] > payload["current_salary"]

def test_invalid_input_validation():
    """Ensure Pydantic schema rejects out-of-bound age inputs (422)."""
    headers = {"X-API-Key": API_KEY}
    payload = {
        "age": 10,  # Below ge=18 constraint
        "years_experience": 2,
        "current_salary": 50000
    }
    
    response = client.post("/analyze-market-value", json=payload, headers=headers)
    assert response.status_code == 422