from typing import List, Optional, Union, Annotated
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import Body
from enum import Enum

# Individual Components


class TimezoneSchema(BaseModel):
    shift_seconds: int = Field(...,
                               description="Shift in seconds for the timezone.")


class LocationSchema(BaseModel):
    cityname: str = Field(..., description="Name of the city.")
    country: Annotated[str,
                       Field(default=None,
                             title="Country Code (alpha-2)",
                             max_length=2)]
    timezone: TimezoneSchema = Field(...,
                                     description="Timezone data for the location.")
    sunrise: int = Field(..., description="Time for sunrise in UNIX format.")
    sunset: int = Field(..., description="Time for sunset in UNIX format.")
    longitude: float = Field(..., description="Longitude of the location.")
    latitude: float = Field(..., description="Latitude of the location.")


class WindSchema(BaseModel):
    speed: float = Field(..., description="Wind speed in meters per second.")
    deg: int = Field(...,
                     description="Wind direction in degrees (meteorological).")
    gust: Optional[float] = Field(
        None, description="Wind gust speed in meters per second.")


class VolumesSchema(BaseModel):
    rain_1h: Optional[float] = Field(
        None, description="Rain volume in the last 1 hour.")
    rain_3h: Optional[float] = Field(
        None, description="Rain volume in the last 3 hours.")
    snow_1h: Optional[float] = Field(
        None, description="Snow volume in the last 1 hour.")
    snow_3h: Optional[float] = Field(
        None, description="Snow volume in the last 3 hours.")


class WeatherMetricsResponse(BaseModel):
    temp: Optional[float]
    wind: WindSchema
    fetch_time: Annotated[datetime | None, Body()] = Field(
        default=None, description="Time when the weather data was fetched.")


class WeatherMetricsSchema(BaseModel):
    temp: float = Field(..., description="Current temperature in Celsius.")
    feels_like: float = Field(...,
                              description="Human perceived temperature in Celsius.")
    pressure: float = Field(..., description="Atmospheric pressure in hPa.")
    humidity: int = Field(..., description="Humidity percentage.")
    visibility: Optional[int] = Field(
        None, description="Visibility in meters.")
    cloudiness: int = Field(..., description="Cloudiness percentage.")
    wind: WindSchema = Field(..., description="Wind details.")
    temp_min: float = Field(..., description="Minimum temperature in Celsius.")
    temp_max: float = Field(..., description="Maximum temperature in Celsius.")
    sea_level: Optional[float] = Field(
        None, description="Sea-level pressure in hPa.")
    grnd_level: Optional[float] = Field(
        None, description="Ground-level pressure in hPa.")


class WeatherSchema(BaseModel):
    main: str = Field(..., description="Main weather condition.")
    description: str = Field(..., description="Detailed weather condition.")
    icon: str = Field(..., description="Weather icon code.")


class CurrentWeatherSchema(BaseModel):
    location: LocationSchema = Field(..., description="Location details.")
    weathers: List[WeatherSchema] = Field(...,
                                          description="List of weather conditions.")
    metrics: WeatherMetricsSchema = Field(..., description="Weather metrics.")
    volume: VolumesSchema = Field(..., description="Precipitation volumes.")
    dt_calculation: int = Field(...,
                                description="Time of weather data calculation in UNIX format.")
    fetch_time: Annotated[datetime | None, Body()] = Field(
        default=None, description="Time when the weather data was fetched.")

# Requests


class Request(BaseModel):
    parameter: Optional[BaseModel] = Field(
        None, description="Request parameter.")

# Responses


class ErrorResponse(BaseModel):
    status: str = Field(..., description="Response status.")
    msg: str = Field(..., description="Response message.")
    result: Optional[BaseModel] = Field(None, description="Response result.")


class ErrorDetails(BaseModel):
    detail: ErrorResponse


class WeatherMetric(str, Enum):
    temp = "temp"
    feels_like = "feels_like"
    pressure = "pressure"
    visibility = "visibility"
    cloudiness = "cloudiness"
    wind_id = "wind_id"
    humidity = "humidity"
    temp_min = "temp_min"
    temp_max = "temp_max"
    sea_level = "sea_level"
    grnd_level = "grnd_level"
    wind = "wind"
