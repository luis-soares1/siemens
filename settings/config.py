from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str
    admin_email: str
    environment: str
    weather_api_key: str
    weather_api_url: str
    job_interval: int
    host: str
    port: int
    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    redis_host: str
    redis_port: int
    redis_is_db: int
    
    model_config = SettingsConfigDict(env_file="prod.env")
    
"""
https://fastapi.tiangolo.com/advanced/settings/#__tabbed_6_1
"""
@lru_cache()
def get_settings():
    return Settings()