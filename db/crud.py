from sqlalchemy.orm import Session
from db.models import (Location, Timezone, Weather, WeatherMetrics, Wind, Volumes, CurrentWeather)
from db.schemas import (TimezoneSchema, LocationSchema, WeatherMetricsSchema, WeatherSchema, WindSchema, VolumesSchema, CurrentWeatherSchema)

# CRUD operations for Location
def create_location(db: Session, location: LocationSchema):
    existing_location = db.query(Location).filter_by(
        cityname=location['longitude'],
        country=location['latitude']
    ).first()
    if existing_location:
        return existing_location
    _location = Location(**location)
    db.add(_location)
    db.commit()
    db.refresh(_location)
    return _location


# CRUD operations for Timezone
def create_timezone(db: Session, timezone: TimezoneSchema):
    existing_timezone = db.query(Timezone).filter_by(shift_seconds=timezone['shift_seconds']).first()
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
    # existing_weather_metrics = db.query(WeatherMetrics).filter_by(main=weather_metrics['main']).first()
    if False:
        return existing_weather_metrics
    _weather_metrics = WeatherMetrics(**weather_metrics)
    db.add(_weather_metrics)
    db.commit()
    db.refresh(_weather_metrics)
    return _weather_metrics


# CRUD operations for Wind
def create_wind(db: Session, wind: WindSchema):
    existing_wind = db.query(Wind).filter_by(
        speed=wind['speed'],
        deg=wind['deg'],
        gust=wind.get('gust', None)  # using get in case 'gust' might not always be provided
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
    # Adjust your filter conditions based on unique criteria for Volumes if necessary
    existing_volume = db.query(Volumes).filter_by(rain_1h=volume.get('rain_1h', None), rain_3h=volume.get('rain_3h', None), snow_1h=volume.get('snow_1h', None), snow_3h=volume.get('snow_3h', None)).first()
    if existing_volume:
        return existing_volume
    _volume = Volumes(**volume)
    db.add(_volume)
    db.commit()
    db.refresh(_volume)
    return _volume

# CRUD operations for CurrentWeather
def get_current_weather(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CurrentWeather).offset(skip).limit(limit).all()

def create_current_weather(db: Session, current_weather: CurrentWeatherSchema):
    existing_current_weather = db.query(CurrentWeather).filter_by(location_id=current_weather['location_id']).first()
    if existing_current_weather:
        return existing_current_weather
    _current_weather = CurrentWeather(**current_weather)
    db.add(_current_weather)
    db.commit()
    db.refresh(_current_weather)
    return _current_weather