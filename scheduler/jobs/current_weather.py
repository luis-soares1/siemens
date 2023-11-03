from common.settings.script_config import script_settings
from datetime import datetime
from common.utils.decorators import retry
from common.utils.normalizer import normalize_api_resp
import requests
from data_manager import data_manager


@retry(max_retries=3, retry_delay=5)
def fetch_external_api(lat: float, lon: float) -> dict:
    url = f"{script_settings.weather_api_url}/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": script_settings.weather_api_key,
        "units": "metric"
    }

    with requests.Session() as r:
        response = r.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        data['fetch_time'] = str(datetime.now())
        data_manager.add_to_batch(normalize_api_resp(data))
