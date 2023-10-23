from fastapi import APIRouter, Query
import requests
import json

router = APIRouter()

router.get("/weather/")
async def get_weather_data(lat: float, lon: float):
    # Get data from database based on GPS coordinates
    weather = session.query(Weather).filter(Weather.coord_lat == lat, Weather.coord_lon == lon).first()
    if not weather:
        raise HTTPException(status_code=404, detail="Data not found for given GPS coordinates")
    return {
        'temperature': weather.temp,
        'wind_speed': weather.wind_speed,
        'fetched_at': weather.dt
    }

router.get("/weather/basic/")
async def get_basic_weather_data(lat: float, lon: float):
    # Get data from database based on GPS coordinates
    weather = session.query(Weather).filter(Weather.coord_lat == lat, Weather.coord_lon == lon).first()
    if not weather:
        raise HTTPException(status_code=404, detail="Data not found for given GPS coordinates")
    return {
        'temperature': weather.temp,
        'wind_speed': weather.wind_speed,
        'fetched_at': weather.dt
    }