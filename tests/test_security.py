def test_predict_missing_api_key_returns_401(client):
    
    payload = {
        
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = client.post("/api/v1/predict", json=payload)
    
    assert response.status_code == 401


def test_predict_invalid_api_key_returns_401(client):
    
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = client.post(
        
        "/api/v1/predict", json=payload, headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401


def test_predict_extra_field_returns_422(client, auth_headers):
    
    payload = {
        
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
        "unexpected_field": "should not be allowed",
    }
    response = client.post("/api/v1/predict", json=payload, headers=auth_headers)
    
    assert response.status_code == 422