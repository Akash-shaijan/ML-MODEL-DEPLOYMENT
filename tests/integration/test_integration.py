import httpx
from app.config import settings


BASE_URL = "http://localhost:8000"

HEADERS = {"X-API-Key": settings.API_KEY}

def test_running_health_endpoint():

    response = httpx.get(f"{BASE_URL}/api/v1/health",timeout=10.0)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    
    assert data["model_loaded"] is True


def test_running_predict_endpoint():

    payload = {
        
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
        
    }

    response = httpx.post(f"{BASE_URL}/api/v1/predict",json=payload,headers=HEADERS,timeout=10.0,)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    
    assert "confidence" in data


def test_running_predict_batch_endpoint():

    payload = {
        
        "inputs": [
            
            {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            },
            
            {
                "sepal_length": 6.0,
                "sepal_width": 2.9,
                "petal_length": 4.5,
                "petal_width": 1.5,
            },
        ]
    }

    response = httpx.post(f"{BASE_URL}/api/v1/predict-batch",json=payload,headers=HEADERS,timeout=10.0,)

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 2


def test_running_metrics_endpoint():

    response = httpx.get(f"{BASE_URL}/metrics",timeout=10.0)

    assert response.status_code == 200

    assert "http_requests_total" in response.text
    
    assert "ml_predictions_total" in response.text