def test_v1_and_v2_return_different_shapes_for_same_input(client,auth_headers):
    
    payload = {
        
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
        
    }

    v1_response = client.post("/api/v1/predict", json=payload,headers=auth_headers)
    
    v2_response = client.post("/api/v2/predict", json=payload,headers=auth_headers) 

    assert v1_response.status_code == 200
    
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    
    v2_data = v2_response.json()

    assert "confidence" in v1_data
    
    assert "probabilities" not in v1_data

    assert "probabilities" in v2_data
    
    assert "confidence" not in v2_data

    assert v1_data["prediction"] == v2_data["prediction"]
    
    