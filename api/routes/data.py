from fastapi import APIRouter, Depends, Body, BackgroundTasks
from api.db.config import get_db, get_settings
from sqlalchemy.orm import Session
from typing import Any
from api.db.crud import create_current_weather

router = APIRouter()


@router.post("/receive_data/weather")
async def receive_latest_data(currentWeatherLocations: Any = Body(...), db: Session = Depends(get_db)):
    for location in currentWeatherLocations:
        create_current_weather(db, location['current_weather'])
