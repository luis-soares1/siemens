from sqlalchemy.orm import Session
from db.models import (
    Location,
    Timezone,
    Weather,
    WeatherMetrics,
    Wind,
    Volumes,
    CurrentWeather)
from db.schemas import (
    TimezoneSchema,
    LocationSchema,
    WeatherMetricsSchema,
    WeatherSchema,
    WindSchema,
    VolumesSchema,
    CurrentWeatherSchema)
from datetime import datetime

# CRUD operations for Location
def create_location(db: Session, location: LocationSchema):
    existing_location = db.query(Location).filter_by(
        longitude=location['longitude'],
        latitude=location['latitude']
    ).first()
    if existing_location:
        return existing_location
    tz = location.pop('timezone')
    _tz = create_timezone(db, tz)
    _location = Location(**location)
    _location.timezone_id = _tz.id
    db.add(_location)
    db.commit()
    db.refresh(_location)
    return _location


# CRUD operations for Timezone
def create_timezone(db: Session, timezone: TimezoneSchema):
    existing_timezone = db.query(Timezone).filter_by(
        shift_seconds=timezone['shift_seconds']).first()
    if existing_timezone:
        return existing_timezone
    _timezone = Timezone(**timezone)
    db.add(_timezone)
    db.commit()
    db.refresh(_timezone)
    return _timezone


# CRUD operations for Weather
def create_weather(db: Session, weather: WeatherSchema):
    existing_weather = db.query(Weather).filter_by(
        id=weather['id']
    ).first()
    if existing_weather:
        return existing_weather
    _weather = Weather(**weather)
    db.add(_weather)
    db.commit()
    db.refresh(_weather)
    return _weather


# CRUD operations for WeatherMetrics
def create_weather_metrics(db: Session, weather_metrics: WeatherMetricsSchema):
    # No query bcuz very unlikely similiar obj. Trade-off not worth it
    wind = weather_metrics.pop('wind')
    _wind = create_wind(db, wind)
    _weather_metrics = WeatherMetrics(**weather_metrics)
    _weather_metrics.wind_id = _wind.id
    db.add(_weather_metrics)
    db.commit()
    db.refresh(_weather_metrics)
    return _weather_metrics


# CRUD operations for Wind
def create_wind(db: Session, wind: WindSchema):
    existing_wind = db.query(Wind).filter_by(
        speed=wind['speed'],
        deg=wind['deg'],
        # using get in case 'gust' might not always be provided
        gust=wind.get('gust', None)
    ).first()
    if existing_wind:
        return existing_wind
    _wind = Wind(**wind)
    db.add(_wind)
    db.commit()
    db.refresh(_wind)
    return _wind

# CRUD operations for Volumes


def create_volumes(db: Session, volume: VolumesSchema):
    # Adjust your filter conditions based on unique criteria for Volumes if
    # necessary
    existing_volume = db.query(Volumes).filter_by(
        rain_1h=volume.get(
            'rain_1h', None), rain_3h=volume.get(
            'rain_3h', None), snow_1h=volume.get(
                'snow_1h', None), snow_3h=volume.get(
                    'snow_3h', None)).first()
    if existing_volume:
        return existing_volume
    _volume = Volumes(**volume)
    db.add(_volume)
    db.commit()
    db.refresh(_volume)
    return _volume

# CRUD operations for CurrentWeather
def create_current_weather(db: Session, current_weather: CurrentWeatherSchema):
    current_weather = current_weather.model_dump()
    loc = create_location(db, current_weather.pop('location'))
    metrics = create_weather_metrics(
        db, current_weather.pop('metrics'))
    vols = create_volumes(db, current_weather.pop('volume'))
    weathers = []
    for weather in current_weather.pop('weathers'):
        weathers.append(create_weather(db, weather))

    _current_weather = CurrentWeather(
        location_id=loc.id,
        weather_metrics_id=metrics.id,
        volume_id=vols.id,
        weathers=weathers,
        fetch_time=current_weather['fetch_time'],
        dt_calculation=current_weather['dt_calculation'])

    db.add(_current_weather)
    db.commit()
    db.refresh(_current_weather)
    return _current_weather
