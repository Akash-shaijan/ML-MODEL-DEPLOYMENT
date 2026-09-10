def test_model_info_returns_expected_keys(client,auth_headers):
    
    response = client.get("/api/v1/model-info",headers=auth_headers)
    
    assert response.status_code == 200
    
    data = response.json()
    
    for key in ["model_type", "version", "trained_on", "features"]:
        
        assert key in data
        
        