from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Из .env 
    MONGO_URI: str = "mongodb://mongo:27017"
    DB_NAME: str = "petdb"
    
    # Из main.py
    NOTIFICATION_SERVICE_URL: str = "http://notification-service:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Синглтон-экземпляр настроек
settings = Settings()