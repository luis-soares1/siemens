from db.config import SessionLocal
from db.models import CurrentWeather, Location
# from db.crud import (get_wind)
from typing import List

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def get_latest_data_query(lat: float, lon: float) -> CurrentWeather:
    db = get_db()
    weather = (
        db.query(CurrentWeather)
        .join(Location, CurrentWeather.location_id == Location.id)  # Assuming there's a foreign key named location_id in CurrentWeather
        .filter(Location.latitude == lat, Location.longitude == lon)
        .order_by(CurrentWeather.id.desc())
        .first()
    )

    print(weather)
    return weather



def get_latest_metrics(
        lat: float,
        lon: float,
        metrics: List[str]) -> dict[str, int | float]:
    db = get_db()
    weather = db.query(CurrentWeather).filter(
        CurrentWeather.location.latitude == lat,
        CurrentWeather.location.longitude == lon).last()
    metrics_to_query = [
        metric for metric in metrics if metric in weather.metrics.keys()]
    return {metric: weather.metrics.keys()[metric]
            for metric in metrics_to_query}
