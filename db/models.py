from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base

class Coordinates(Base):
    __tablename__ = 'coords'
    coord_id = Column(Integer, primary_key=True)
    lon = Column(Float)
    lat = Column(Float)

class Weather(Base):
    __tablename__ = 'weather'
    weather_id = Column(Integer, primary_key=True)
    main = Column(String)
    description = Column(String)
    icon = Column(String)

class MainWeatherDetails(Base):
    __tablename__ = 'main_weather_details'
    main_weather_id = Column(Integer, primary_key=True)
    temp = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)

class Wind(Base):
    __tablename__ = 'wind'
    wind_id = Column(Integer, primary_key=True)
    speed = Column(Float)
    deg = Column(Integer)

class Clouds(Base):
    __tablename__ = 'clouds'
    cloud_id = Column(Integer, primary_key=True)
    all = Column(Integer)

class SystemDetails(Base):
    __tablename__ = 'system_details'
    sys_id = Column(Integer, primary_key=True)
    type = Column(Integer)
    id = Column(Integer)
    country = Column(String)
    sunrise = Column(Integer)
    sunset = Column(Integer)

class Location(Base):
    __tablename__ = 'location'
    location_id = Column(Integer, primary_key=True)
    name = Column(String)
    coord_id = Column(Integer, ForeignKey('coords.coord_id'))
    weather_id = Column(Integer, ForeignKey('weather.weather_id'))
    main_weather_id = Column(Integer, ForeignKey('main_weather_details.main_weather_id'))
    wind_id = Column(Integer, ForeignKey('wind.wind_id'))
    cloud_id = Column(Integer, ForeignKey('clouds.cloud_id'))
    sys_id = Column(Integer, ForeignKey('system_details.sys_id'))
    base = Column(String)
    visibility = Column(Integer)
    dt = Column(Integer)
    timezone = Column(Integer)
    cod = Column(Integer)
    
    # verificar se backref é correto. ver a documentaçao atual
    coords_rel = relationship("Coordinates", backref="location")
    weather_rel = relationship("Weather", backref="location")
    main_weather_details_rel = relationship("MainWeatherDetails", backref="location")
    wind_rel = relationship("Wind", backref="location")
    cloud_rel = relationship("Clouds", backref="location")
    system_details_rel = relationship("SystemDetails", backref="location")