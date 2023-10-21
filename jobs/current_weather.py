import requests
from settings.config import Settings

settings = Settings()

def get_current_weather_data():
    try:
        response = requests.get(f"{settings.api_url}/weather?lat=38.7320286&lon=-9.217414&appid={settings.api_key}")
        response.raise_for_status()
        # Process response ----> store the data after
    except requests.RequestException as e:
        print(f"Error during request: {e}")