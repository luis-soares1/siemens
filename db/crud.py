from sqlalchemy.orm import Session
from .models import (Coordinates, Weather, MainWeatherDetails, Wind, Clouds, SystemDetails, Location)
from .schemas import (CoordinatesSchema, WeatherSchema, MainWeatherDetailsSchema, WindSchema, CloudsSchema, SystemDetailsSchema, LocationSchema)

# CRUD operations for Coordinates
def get_coordinates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Coordinates).offset(skip).limit(limit).all()

def create_coordinates(db: Session, coords: CoordinatesSchema):
    _coords = Coordinates(**coords.model_dump())
    db.add(_coords)
    db.commit()
    db.refresh(_coords)
    return _coords

# CRUD operations for Weather
def get_weather(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Weather).offset(skip).limit(limit).all()

def create_weather(db: Session, weather: WeatherSchema):
    _weather = Weather(**weather.model_dump())
    db.add(_weather)
    db.commit()
    db.refresh(_weather)
    return _weather

# CRUD operations for MainWeatherDetails
def get_main_weather_details(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MainWeatherDetails).offset(skip).limit(limit).all()

def create_main_weather_details(db: Session, details: MainWeatherDetailsSchema):
    _details = MainWeatherDetails(**details.model_dump())
    db.add(_details)
    db.commit()
    db.refresh(_details)
    return _details

# CRUD operations for Wind
def get_wind(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Wind).offset(skip).limit(limit).all()

def create_wind(db: Session, wind: WindSchema):
    _wind = Wind(**wind.model_dump())
    db.add(_wind)
    db.commit()
    db.refresh(_wind)
    return _wind

# CRUD operations for Clouds
def get_clouds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Clouds).offset(skip).limit(limit).all()

def create_clouds(db: Session, cloud: CloudsSchema):
    _cloud = Clouds(**cloud.model_dump())
    db.add(_cloud)
    db.commit()
    db.refresh(_cloud)
    return _cloud

# CRUD operations for SystemDetails
def get_system_details(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SystemDetails).offset(skip).limit(limit).all()

def create_system_details(db: Session, system: SystemDetailsSchema):
    _system = SystemDetails(**system.model_dump())
    db.add(_system)
    db.commit()
    db.refresh(_system)
    return _system

# CRUD operations for Location
def get_location(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location).offset(skip).limit(limit).all()

def get_location_by_id(db: Session, location_id: int):
    return db.query(Location).filter(Location.location_id == location_id).first()

def create_location(db: Session, location: LocationSchema):
    _location = Location(**location.model_dump())
    db.add(_location)
    db.commit()
    db.refresh(_location)
    return _location

def remove_location(db: Session, location_id: int):
    _location = get_location_by_id(db=db, location_id=location_id)
    db.delete(_location)
    db.commit()

def update_location(db: Session, location_id: int, location_update: LocationSchema):
    _location = get_location_by_id(db=db, location_id=location_id)
    for key, value in location_update.model_dump().items():
        setattr(_location, key, value)
    db.commit()
    db.refresh(_location)
    return _location
