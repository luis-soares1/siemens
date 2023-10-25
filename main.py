from fastapi import FastAPI
from core.core import Core
from routes.weather import router as weather_router

app = FastAPI()
app.include_router(weather_router, tags=["weather"])
routes = [route for route in app.routes]
print(routes)

try:
    core = Core()
    core.load_locations()
except Exception as e:
    print('Error launching algorithm', e)
    
