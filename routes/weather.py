from fastapi import APIRouter, HTTPException, Depends
from db.query import get_latest_data_query
from db.config import get_db
from sqlalchemy.orm import Session
from middleware import cache

router = APIRouter()


@router.get("/weather/")
async def get_latest_data(lat: float, lon: float, db: Session = Depends(get_db)):
    print(lat, lon)
    # key = f"latest_weather_{lat}_{lon}"
    # is_cached = await cache.get(key)
    # if not is_cached:
    weather = get_latest_data_query(lat=lat, lon=lon, db=db)
        # cache.put(key, weather)
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