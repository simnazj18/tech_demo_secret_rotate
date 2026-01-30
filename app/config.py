import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_KEYVAULT_URL: str
    KUBERNETES_NAMESPACE: str = "default"  # Default to 'default' namespace or 'all'
    
    class Config:
        env_file = ".env"

settings = Settings()
