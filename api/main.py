import uvicorn
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from routes.weather import router as weather_router
from routes.data import router as data_router
from middleware.cache import cache
from common.settings.config import app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cache lifecycle
    await cache.create_redis_pool()
    yield
    await cache.close_redis_pool()

try:
    docs_url = None if not app_settings.debug else "/docs"
    redoc_url = None if not app_settings.debug else "/redoc"
    openapi_url = None if not app_settings.debug else "/openapi.json"
    app = FastAPI(
        title=app_settings.app_name,
        description=app_settings.app_description,
        lifespan=lifespan,
        debug=app_settings.debug,
        docs_url=docs_url,
        redoc_url=redoc_url)
    app.include_router(weather_router, tags=["weather"])
    app.include_router(data_router, tags=["data"])
    uvicorn.run(app, host=app_settings.host, port=app_settings.port)
except Exception as e:
    print('Error launching algorithm', e)
