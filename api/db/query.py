from db.models import CurrentWeather, Location
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from common.utils.utils import METRIC_EXTRACTION_MAP


async def get_latest_data_query(
        lat: float,
        lon: float,
        db: Session) -> CurrentWeather:
    weather = (
        db.query(CurrentWeather)
        .join(Location, CurrentWeather.location_id == Location.id)
        .filter(Location.latitude == lat, Location.longitude == lon)
        .order_by(CurrentWeather.fetch_time.desc())
        .first()
    )
    
    return weather


async def get_latest_metrics_query(
        lat: float,
        lon: float,
        metrics: List[str],
        db: Session
) -> Dict[str, Union[int, float, None]]:

    weather_entry = await get_latest_data_query(lat, lon, db)
    
    # No actual results on the db
    if not weather_entry:
        return {}

    # Get all metrics
    if not metrics:
        weather_entry.metrics.fetch_time = weather_entry.fetch_time
        return weather_entry.metrics
    
    # Get some metrics
    result = {}
    for metric in metrics:
        if hasattr(weather_entry.metrics, metric):
            result[metric] = getattr(weather_entry.metrics, metric)
    
    # Wrong metrics, even though FastAPI will check for them first.
    if len(result) == 0:
        return {}

    result['fetch_time'] = weather_entry.fetch_time
    return result
