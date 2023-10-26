from db.config import SessionLocal
from db.models import CurrentWeather, Location
from sqlalchemy.orm import Session
from typing import List


def get_latest_data_query(lat: float, lon: float, db: Session) -> CurrentWeather:
    weather = (
        db.query(CurrentWeather)
        .join(Location, CurrentWeather.location_id == Location.id)
        .filter(Location.latitude == lat, Location.longitude == lon)
        .order_by(CurrentWeather.fetch_time.desc())
        .first()
    )
    
    return weather

def get_latest_metrics(
        lat: float,
        lon: float,
        metrics: List[str],
        db: Session
        ) -> dict[str, int | float]:
    weather = db.query(CurrentWeather).filter(
        CurrentWeather.location.latitude == lat,
        CurrentWeather.location.longitude == lon).last()
    metrics_to_query = [
        metric for metric in metrics if metric in weather.metrics.keys()]
    return {metric: weather.metrics.keys()[metric]
            for metric in metrics_to_query}
