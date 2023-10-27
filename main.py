from core.core import Core
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.weather import router as weather_router
from middleware.cache import create_redis_pool, close_redis_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cache lifecycle
    await create_redis_pool()
    yield
    await close_redis_pool()

try:
    app = FastAPI(lifespan=lifespan)
    app.include_router(weather_router, tags=["weather"])
    core = Core()
    core.run()
except Exception as e:
    print('Error launching algorithm', e)
    
