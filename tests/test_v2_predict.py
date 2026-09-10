def test_v2_predict_valid_input_returns_200(client,auth_headers):
    
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = client.post("/api/v2/predict", json=payload,headers=auth_headers) 
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert "probabilities" in data
    
    assert set(data["probabilities"].keys()) == {"setosa", "versicolor", "virginica"}
    
    assert abs(sum(data["probabilities"].values()) - 1.0) < 0.01



def test_v2_predict_missing_field_returns_422(client,auth_headers):
    
    payload = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4}
    
    response = client.post("/api/v2/predict", json=payload,headers=auth_headers)
    
    assert response.status_code == 422 

    