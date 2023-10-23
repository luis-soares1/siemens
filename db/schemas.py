from typing import List, Optional
from pydantic import BaseModel, Field

# Individual Components

class TimezoneSchema(BaseModel):
    id: Optional[int]
    shift_seconds: int

    class Config:
        from_attributes = True

class LocationSchema(BaseModel):
    id: Optional[int]
    cityname: str
    country: str
    timezone: TimezoneSchema
    sunrise: int
    sunset: int
    longitude: float
    latitude: float

    class Config:
        from_attributes = True
        

class WindSchema(BaseModel):
    id: Optional[int]
    speed: float
    deg: int
    gust: Optional[float]

    class Config:
        from_attributes = True

class VolumesSchema(BaseModel):
    id: Optional[int]
    rain_1h: Optional[float]
    rain_3h: Optional[float]
    snow_1h: Optional[float]
    snow_3h: Optional[float]

    class Config:
        from_attributes = True

class WeatherMetricsSchema(BaseModel):
    id: Optional[int]
    temp: float
    feels_like: float
    pressure: float
    humidity: int
    visibility: int
    cloudiness: int
    wind: WindSchema
    temp_min: float
    temp_max: float
    sea_level: float
    grnd_level: float

    class Config:
        from_attributes = True

class WeatherSchema(BaseModel):
    id: Optional[int]
    main: str
    description: str
    icon: str

    class Config:
        from_attributes = True
class CurrentWeatherSchema(BaseModel):
    id: Optional[int]
    location: LocationSchema
    weathers: List[WeatherSchema]   # Note the change here
    weather_metrics: WeatherMetricsSchema  # Including the metrics directly for a more comprehensive response
    volume: VolumesSchema
    dt_calculation: int

    class Config:
        from_attributes = True

# Requests 

class Request(BaseModel):
    parameter: Optional[BaseModel]

# Responses

class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[BaseModel]
