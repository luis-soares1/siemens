from typing import Union
from fastapi import FastAPI, Depends
from scheduler.scheduler import ApiScheduler
# from api.apiservice import ApiService
from settings import config
from functools import lru_cache
from typing_extensions import Annotated
# from routers import weather
from db.config import engine
from db import models
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logger

scheduler = AsyncIOScheduler(job_defaults={'log': logger, 'misfire_grace_time': 15*60})
scheduler.start()

def my_job():
    print("Job is running...")

scheduler.add_job(my_job, 'interval', seconds=5)


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()
# app.include_router(weather.router)


# scheduler = ApiScheduler()
# api = ApiService()
# scheduler.create_job(api.get_current_weather)

"""
https://fastapi.tiangolo.com/advanced/settings/#__tabbed_6_1
"""
@lru_cache()
def get_settings():
    return config.Settings()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "routes": [{"path": route.path, "name": route.name} for route in app.routes]
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

