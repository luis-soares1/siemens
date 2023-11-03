from db.models import CurrentWeather, Location, WeatherMetrics
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Union, Dict


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

async def get_avg_across_locations(db: Session) -> int:
    location_and_temp_list = (
        db.query(
            CurrentWeather.location_id,
            WeatherMetrics.temp.label('temp')
        )
        # get all metrics, sort by date and apply distinct. All next occurrences (older) are removed
        .join(WeatherMetrics, WeatherMetrics.id == CurrentWeather.weather_metrics_id)
        .order_by(CurrentWeather.location_id, CurrentWeather.fetch_time.desc())
        .distinct(CurrentWeather.location_id)
        .all()
    )

    return sum([temp for _, temp in location_and_temp_list])/len(location_and_temp_list)

    # OLD APPROACH

    # return average_temp_query
    # print('called avg')
    # location_len = len(db.query(Location).all())
    # recent_data = db.query(CurrentWeather).order_by(CurrentWeather.fetch_time.desc()).limit(location_len).all()
    
    # print(recent_data, 'here')
    # sum = 0
    # for location in recent_data:
    #     print(location)
    #     sum += location.metrics.temp
    
    # return sum/location_len
    
    
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
