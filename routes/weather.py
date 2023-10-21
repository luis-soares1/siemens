from fastapi import APIRouter, Query
import requests
import json

router = APIRouter()

@router.get("/weather", tags=["weather"])
async def get_current_weather(lat: float, lng: float):
    try:
        data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid=d2885c3159b8754fffbec7bfd235154c")       
        return data
    except:
        print('couldnt handle request.')