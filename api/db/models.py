from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.config import Base

# Association table for Weather and CurrentWeather
weather_association = Table(
    'weather_association', Base.metadata, Column(
        'current_weather_id', Integer, ForeignKey('current_weather.id')), Column(
            'weather_id', Integer, ForeignKey('weather.id')))


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    cityname = Column(String)
    country = Column(String)
    timezone_id = Column(Integer, ForeignKey('timezone.id'))
    sunrise = Column(Integer)
    sunset = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)

    timezone = relationship("Timezone", lazy="joined")


class Timezone(Base):
    __tablename__ = 'timezone'
    id = Column(Integer, primary_key=True)
    shift_seconds = Column(Integer)  # Shift from UTC


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    main = Column(String)
    description = Column(String)
    icon = Column(String)

    current_weathers = relationship(
        "CurrentWeather",
        secondary=weather_association,
        back_populates="weathers",
        lazy="joined")


class WeatherMetrics(Base):
    __tablename__ = 'weather_metrics'
    id = Column(Integer, primary_key=True)
    temp = Column(Float)
    feels_like = Column(Float)
    pressure = Column(Float)
    visibility = Column(Integer)
    cloudiness = Column(Integer)
    wind_id = Column(Integer, ForeignKey('wind.id'))
    humidity = Column(Integer)
    temp_min = Column(Float)
    temp_max = Column(Float)
    sea_level = Column(Float)
    grnd_level = Column(Float)

    wind = relationship("Wind", backref="weather_metrics", lazy="joined")


class Wind(Base):
    __tablename__ = 'wind'
    id = Column(Integer, primary_key=True)
    speed = Column(Float)
    deg = Column(Integer)
    gust = Column(Float)


class Volumes(Base):
    __tablename__ = 'volumes'
    id = Column(Integer, primary_key=True)
    rain_1h = Column(Float)
    rain_3h = Column(Float)
    snow_1h = Column(Float)
    snow_3h = Column(Float)


class CurrentWeather(Base):
    __tablename__ = 'current_weather'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'))
    weather_metrics_id = Column(Integer, ForeignKey('weather_metrics.id'))
    volume_id = Column(Integer, ForeignKey('volumes.id'))
    fetch_time = Column(DateTime)
    dt_calculation = Column(Integer)

    location = relationship("Location", lazy="joined")
    metrics = relationship("WeatherMetrics", lazy="joined")
    weathers = relationship(
        "Weather",
        secondary=weather_association,
        back_populates="current_weathers",
        lazy="joined")
    volume = relationship("Volumes", lazy="joined")
