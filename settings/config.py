from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Weather App"
    admin_email: str = "luis.soares@campus.ul.pt"
    api_key: str
    api_url: str
    environment: str
    
    model_config = SettingsConfigDict(env_file="prod.env")
