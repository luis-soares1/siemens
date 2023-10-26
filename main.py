from fastapi import FastAPI
from core.core import Core
from routes.weather import router as weather_router

app = FastAPI()

try:
    app.include_router(weather_router, tags=["weather"])
    core = Core()
    core.run()
except Exception as e:
    print('Error launching algorithm', e)
    
