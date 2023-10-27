from fastapi import APIRouter, HTTPException, Depends
from db.query import get_latest_data_query, get_latest_metrics_query
from db.config import get_db, get_settings
from sqlalchemy.orm import Session
from middleware import cache

router = APIRouter()
settings= get_settings()

@router.get("/weather")
async def get_latest_data(lat: float, lon: float, db: Session = Depends(get_db)):
    key = f"latest_weather_{lat}_{lon}"
    weather = await cache.get(key)
    if not weather:
        weather = get_latest_data_query(lat=lat, lon=lon, db=db)
        await cache.put(key, weather, settings.job_interval)
        if not weather:
            raise HTTPException(status_code=404, detail="Data not found for given GPS coordinates")
    print(weather.location)
    return weather


@router.get("/weather_metrics")
async def get_latest_metrics(lat: float, lon: float, db: Session = Depends(get_db)):
    key = f"latest_weather_metrics_{lat}_{lon}"
    obj = await cache.get(key)
    if not obj:
        obj = get_latest_metrics_query(lat=lat, lon=lon, db=db, metrics=['wind', 'temp'])
        await cache.put(key, obj, settings.job_interval)
        if not obj:
            raise HTTPException(status_code=404, detail="Data not found for given GPS coordinates")
    return obj