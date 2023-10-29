from settings.config import settings
from datetime import datetime
from utils.decorators import retry
from utils.normalizer import normalize_api_resp
import requests
from data_manager import data_manager

@retry(max_retries=3, retry_delay=5)
def fetch_and_populate(lat: float, lon: float) -> dict:
    url = f"{settings.weather_api_url}/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.weather_api_key,
        "units": "metric"
    }
    
    with requests.Session() as r:
        response = r.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        data['timestamp_fetched'] = str(datetime.now())
        data_manager.add_to_batch(normalize_api_resp(data))
