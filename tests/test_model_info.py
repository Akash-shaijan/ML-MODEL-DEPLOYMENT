def test_model_info_returns_expected_keys(client):
    
    response = client.get("/api/v1/model-info")
    
    assert response.status_code == 200
    
    data = response.json()
    
    for key in ["model_type", "version", "trained_on", "features"]:
        
        assert key in data
        
        