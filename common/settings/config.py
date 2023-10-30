from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


def get_app_env_path():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ENV_PATH = os.path.join(BASE_DIR, "api", ".env")
    return ENV_PATH

class AppSettings(BaseSettings):
    app_name: str
    app_description: str
    admin_email: str
    environment: str
    debug: bool
    host: str
    port: int
    db_host: str
    cache_host: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    redis_host: str
    redis_port: int
    redis_is_db: int

    model_config = SettingsConfigDict(env_file=get_app_env_path())

"""
https://fastapi.tiangolo.com/advanced/settings/#__tabbed_6_1
"""


@lru_cache()
def get_app_settings():
    return AppSettings()


app_settings = get_app_settings()
