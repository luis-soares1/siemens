# from core.core import Core
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.weather import router as weather_router
from routes.data import router as data_router
from middleware.cache import create_redis_pool, close_redis_pool
from settings.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cache lifecycle
    await create_redis_pool()
    yield
    await close_redis_pool()

try:
    docs_url = None if not settings.debug else "/docs"
    redoc_url = None if not settings.debug else "/redoc"
    openapi_url = None if not settings.debug else "/openapi.json"
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        lifespan=lifespan,
        debug=settings.debug,
        docs_url=docs_url,
        redoc_url=redoc_url)
    app.include_router(weather_router, tags=["weather"])
    app.include_router(data_router, tags=["data"])
    uvicorn.run(app, host=settings.host, port=settings.port)
except Exception as e:
    print('Error launching algorithm', e)
