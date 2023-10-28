import httpx
from settings.config import get_settings
from fastapi import Depends
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends
# from utils.decorators import retry
from datetime import datetime
from utils.normalizer import normalize_api_resp
import requests
from data_manager import data_manager


settings = get_settings()

# @retry(max_retries=3, retry_delay=5)
def fetch_and_populate(lat: float, lon: float) -> dict:
    # Ver se é possivel adicionar alguma timestamp ao proprio cliente.
    # ver se quando o request é successful ou algo assim, se podemos
    # dar trigger a uma açao
    with requests.Session() as s:
        url = f"{settings.weather_api_url}/weather?lat={lat}&lon={lon}&appid={settings.weather_api_key}&units=metric"
        response = s.get(url)
        print(lat, lon, "<---- Fetched")
        response.raise_for_status()
        # s.post(f"{settings.host}:{settings.port}", response.json())
        data_manager.add_to_batch(response.json())