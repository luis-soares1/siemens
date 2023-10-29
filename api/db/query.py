from db.config import SessionLocal
from db.models import CurrentWeather, Location
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from utils.utils import extract_wind_data, extract_temp_data, METRIC_EXTRACTION_MAP


def get_latest_data_query(lat: float, lon: float, db: Session) -> CurrentWeather:
    weather = (
        db.query(CurrentWeather)
        .join(Location, CurrentWeather.location_id == Location.id)
        .filter(Location.latitude == lat, Location.longitude == lon)
        .order_by(CurrentWeather.fetch_time.desc())
        .first()
    )
    
    return weather

def get_latest_metrics_query(
        lat: float,
        lon: float,
        metrics: List[str],
        db: Session
        ) -> Dict[str, Union[int, float, None]]:
    
    weather_entry = get_latest_data_query(lat, lon, db)
    print(metrics)

    if not weather_entry:
        return {}

    result = {}
    for metric in metrics:
        if metric in METRIC_EXTRACTION_MAP:
            result[metric] = METRIC_EXTRACTION_MAP[metric](weather_entry.metrics)
    result['fetch_time'] = weather_entry.fetch_time
    return result