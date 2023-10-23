from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str
    admin_email: str
    weather_api_key: str
    weather_api_url: str
    environment: str
    job_interval: int
    host: str
    port: int
    
    model_config = SettingsConfigDict(env_file="prod.env")
    
"""
https://fastapi.tiangolo.com/advanced/settings/#__tabbed_6_1
"""
@lru_cache()
def get_settings():
    return Settings()