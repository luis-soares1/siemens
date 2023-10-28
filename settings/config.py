from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

def get_env_path():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ENV_PATH = os.path.join(BASE_DIR, "prod.env")
    return ENV_PATH

class Settings(BaseSettings):
    app_name: str
    admin_email: str
    environment: str
    debug: bool
    weather_api_key: str
    weather_api_url: str
    job_interval: int
    misfire_grace_time: int
    host: str
    port: int
    postgres_db: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    redis_host: str
    redis_port: int
    redis_is_db: int
    
    model_config = SettingsConfigDict(env_file=get_env_path())
    
"""
https://fastapi.tiangolo.com/advanced/settings/#__tabbed_6_1
"""
@lru_cache()
def get_settings():
    return Settings()