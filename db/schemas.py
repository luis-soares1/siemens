from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class CoordinatesSchema(BaseModel):
    coord_id: Optional[int]
    lon: float
    lat: float

    class Config:
        orm_mode = True

class WeatherSchema(BaseModel):
    weather_id: Optional[int]
    main: str
    description: str
    icon: str

    class Config:
        orm_mode = True

class MainWeatherDetailsSchema(BaseModel):
    main_weather_id: Optional[int]
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int

    class Config:
        orm_mode = True

class WindSchema(BaseModel):
    wind_id: Optional[int]
    speed: float
    deg: int

    class Config:
        orm_mode = True

class CloudsSchema(BaseModel):
    cloud_id: Optional[int]
    all: int

    class Config:
        orm_mode = True

class SystemDetailsSchema(BaseModel):
    sys_id: Optional[int]
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int

    class Config:
        orm_mode = True

class LocationSchema(BaseModel):
    location_id: Optional[int]
    name: str
    coord_id: int
    weather_id: int
    main_weather_id: int
    wind_id: int
    cloud_id: int
    sys_id: int
    base: str
    visibility: int
    dt: int
    timezone: int
    cod: int

    class Config:
        orm_mode = True

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    
class RequestCoordinates(BaseModel):
    parameter: CoordinatesSchema = Field(...)
    
class RequestWeather(BaseModel):
    parameter: WeatherSchema = Field(...)
    
class RequestMainWeatherDetails(BaseModel):
    parameter: MainWeatherDetailsSchema = Field(...)
    
class RequestWind(BaseModel):
    parameter: WindSchema = Field(...)

class RequestClouds(BaseModel):
    parameter: CloudsSchema = Field(...)
    
class RequestSystemDetails(BaseModel):
    parameter: CloudsSchema = Field(...)
    
class RequestLocation(BaseModel):
    parameter: CloudsSchema = Field(...)
