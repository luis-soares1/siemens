from fastapi import APIRouter, Depends, Query
from typing import Annotated, List
from api.db.query import get_latest_data_query, get_latest_metrics_query, get_avg_across_locations
from api.db.config import get_db
from common.utils.exceptions import NoDataException
from api.db.schemas import CurrentWeatherSchema, WeatherMetricsResponse, WeatherMetric
from sqlalchemy.orm import Session
from middleware.cache import cache

router = APIRouter(prefix="/v1")


@router.get("/weather", response_model=CurrentWeatherSchema,
            response_model_exclude_none=True)
async def get_latest_data(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude of the location")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude of the location")],
    db: Session =
    Depends(get_db)
) -> CurrentWeatherSchema:

    try:
        key = f"latest_weather_{lat}_{lon}"
        weather = await cache.get(key)
        if not weather:
            weather = await get_latest_data_query(lat=lat, lon=lon, db=db)
            if not weather:
                raise NoDataException()
        return weather
    finally:
        await cache.put(key, weather, ttl=5 * 60)


@router.get("/weather_metrics",
            response_model=WeatherMetricsResponse,
            response_model_exclude_none=True)
async def get_latest_metrics(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude of the location")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude of the location")],
    metrics: List[WeatherMetric] = Query(default=None, description="A set of metrics to query"),
    db: Session = Depends(get_db)
) -> WeatherMetricsResponse:

    key = f"latest_weather_metrics_{lat}_{lon}_{'_'.join(metrics) if metrics else ''}"
    try:
        weather_metrics = await cache.get(key)
        if not weather_metrics:
            weather_metrics = await get_latest_metrics_query(lat=lat, lon=lon, db=db, metrics=metrics)
            if not weather_metrics:
                raise NoDataException()
        return weather_metrics
    finally:
        await cache.put(key, weather_metrics, ttl=5 * 60)
        
        
@router.get("/weather_avg")
async def get_avg(db: Session = Depends(get_db)):
    try:
        data = await get_avg_across_locations(db)
        print(data)
        return data
    except Exception as e:
        print(e)
        return(e, "Exception")
