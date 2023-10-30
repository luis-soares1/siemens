from db.models import CurrentWeather, Location
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from common.utils.utils import METRIC_EXTRACTION_MAP


def get_latest_data_query(
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


def get_latest_metrics_query(
        lat: float,
        lon: float,
        metrics: List[str],
        db: Session
) -> Dict[str, Union[int, float, None]]:

    weather_entry = get_latest_data_query(lat, lon, db)
    print(metrics)

    # No coordinates
    if not weather_entry:
        return {"error": "Data not found for given GPS coordinates"}

    result = {}
    for metric in metrics:
        if metric in METRIC_EXTRACTION_MAP:
            result[metric] = METRIC_EXTRACTION_MAP[metric](
                weather_entry.metrics)

    # Coordinates but no/wrong metrics.
    if len(result) == 0:
        return {"error": "Queried metrics are not available"}

    result['fetch_time'] = weather_entry.fetch_time
    return result
