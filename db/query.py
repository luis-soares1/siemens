from sqlalchemy.orm import Session
from db.models import CurrentWeather
from db.crud import (get_wind)
from typing import List


def get_latest_data(db: Session, lat: float, lon: float) -> CurrentWeather:
    weather = db.query(CurrentWeather).filter(
        CurrentWeather.location.latitude == lat,
        CurrentWeather.location.longitude == lon).last()
    return weather


def get_latest_metrics(
        db: Session,
        lat: float,
        lon: float,
        metrics: List[str]) -> dict[str, int | float]:
    weather = db.query(CurrentWeather).filter(
        CurrentWeather.location.latitude == lat,
        CurrentWeather.location.longitude == lon).last()
    metrics_to_query = [
        metric for metric in metrics if metric in weather.metrics.keys()]
    return {metric: weather.metrics.keys()[metric]
            for metric in metrics_to_query}
