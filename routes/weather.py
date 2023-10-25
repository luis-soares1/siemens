from fastapi import APIRouter, HTTPException
from db.query import get_latest_data_query, get_latest_metrics

router = APIRouter()

@router.get("/weather/")
def get_latest_data(lat: float, lon: float):
    weather = get_latest_data_query(lat, lon)
    print(weather)
    if not weather:
        raise HTTPException(status_code=404, detail="Data not found for given GPS coordinates")
    print(weather.location)
    return weather

# router.get("/weather")
# async def get_latest_metrics(lat: float, lon: float):
#     # Get data from database based on GPS coordinates
#     weather = session.query(Weather).filter(Weather.coord_lat == lat, Weather.coord_lon == lon).first()
#     if not weather:
#         raise HTTPException(status_code=404, detail="Data not found for given GPS coordinates")
#     return {
#         'temperature': weather.temp,
#         'wind_speed': weather.wind_speed,
#         'fetched_at': weather.dt
#     }
    
# router.get("/weather/basic/")
# async def get_basic_weather_data(lat: float, lon: float):
#     # Get data from database based on GPS coordinates
#     weather = session.query(Weather).filter(Weather.coord_lat == lat, Weather.coord_lon == lon).first()
#     if not weather:
#         raise HTTPException(status_code=404, detail="Data not found for given GPS coordinates")
#     return {
#         'temperature': weather.temp,
#         'wind_speed': weather.wind_speed,
#         'fetched_at': weather.dt
#     }