from fastapi import APIRouter, Depends, Body, BackgroundTasks
from api.db.schemas import CurrentWeatherSchema
from api.db.config import get_db
from sqlalchemy.orm import Session
from api.db.crud import create_current_weather
from middleware.cache import cache

router = APIRouter()


@router.post("/receive_data/weather")
async def receive_latest_data(currentWeatherLocations: list[CurrentWeatherSchema], db: Session = Depends(get_db)):
    for location in currentWeatherLocations:
        create_current_weather(db, location)
    # New data, clear all cached keys to avoid returning wrong results
    # previously cached
    await cache.clear_all_cache()
