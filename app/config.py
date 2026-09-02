from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    API_TITLE: str = "ML Model Deployment as a Monitored REST API"
    
    MODEL_PATH: str = "ml/saved_model/model.joblib"
    
    MODEL_METADATA_PATH: str = "ml/saved_model/model_metadata.json"
    
    LOG_LEVEL: str = "INFO"
    
    MAX_BATCH_SIZE: int = 100


settings = Settings() 

