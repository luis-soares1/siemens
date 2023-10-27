import httpx
from settings.config import get_settings
from fastapi import Depends
from db.config import get_db
import requests
from db.crud import (
    create_location,
    create_timezone,
    create_weather,
    create_weather_metrics,
    create_wind,
    create_volumes,
    create_current_weather
    )
from db.config import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from utils.decorators import retry
from datetime import datetime


# @retry(max_retries=3, retry_delay=5)
async def get_current_weather_data(lat: float, lon: float) -> None:    
    settings = get_settings()
    db = SessionLocal()
    url = f"{settings.weather_api_url}/weather?lat={lat}&lon={lon}&appid={settings.weather_api_key}&units=metric"
    data = await fetch_weather_data(url)
    print(lat, lon)
    try:
        await save_weather_data_to_db(db, data)
        db.close()
    except Exception as e:
        db.rollback()
        print(f"Error saving to database: {e}")
        raise
    finally:
        db.close()


async def fetch_weather_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def save_weather_data_to_db(db, data: dict) -> None:
    timestamp_fetched = datetime.now()

    location_obj = create_location(db, {
        'cityname': data['name'],
        'country': data['sys']['country'],
        'timezone_id': create_timezone(db, {'shift_seconds': data['timezone']}).id,
        'sunrise': data['sys']['sunrise'],
        'sunset': data['sys']['sunset'],
        'longitude': round(data['coord']['lon'], ndigits=3),
        'latitude': round(data['coord']['lat'], ndigits=3)
    })

    volume_obj = create_volumes(db, {
        # Check existence of keys rain/snow and hours. If exists, return
        # values, else return None
        'rain_1h': data['rain']['1h'] if data.get('rain', {}).get('1h') else None,
        'rain_3h': data['rain']['3h'] if data.get('rain', {}).get('3h') else None,
        'snow_1h': data['snow']['1h'] if data.get('snow', {}).get('1h') else None,
        'snow_3h': data['snow']['3h'] if data.get('snow', {}).get('3h') else None
    })

    wind_obj = create_wind(db, {
        'speed': data['wind']['speed'],
        'deg': data['wind'].get('deg', None),
        'gust': data['wind'].get('gust', None)
    })

    weather_metrics_obj = create_weather_metrics(db, {
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'pressure': data['main']['pressure'],
        # some APIs might not always provide this
        'visibility': data.get('visibility', None),
        'cloudiness': data['clouds']['all'],
        'wind_id': wind_obj.id,
        'humidity': data['main']['humidity'],
        'temp_min': data['main']['temp_min'],
        'temp_max': data['main']['temp_max'],
        # sea level might not be provided
        'sea_level': data['main'].get('sea_level', None),
        # ground level might not be provided
        'grnd_level': data['main'].get('grnd_level', None)
    })

    current_weather = create_current_weather(db, {
        'fetch_time': timestamp_fetched,
        'dt_calculation': data['dt'],
        'location_id': location_obj.id,
        'weather_metrics_id': weather_metrics_obj.id,
        'volume_id': volume_obj.id
    })


    weather_objects = []
    for weather in data['weather']:
        weather_obj = create_weather(db, {
            'id': weather['id'],
            'main': weather['main'],
            'description': weather['description'],
            'icon': weather['icon'],
        })
        weather_objects.append(weather_obj)

    current_weather.weathers = weather_objects
    db.commit()
    db.refresh(current_weather)
