import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


def get_script_env_path():
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))
    ENV_PATH = os.path.join(BASE_DIR, "scheduler", ".env")
    return ENV_PATH


class ScriptSettings(BaseSettings):
    host: str
    port: int
    weather_api_key: str
    weather_api_url: str
    job_interval: int
    misfire_grace_time: int
    model_config = SettingsConfigDict(env_file=get_script_env_path())


@lru_cache()
def get_script_settings():
    return ScriptSettings()


script_settings = get_script_settings()
