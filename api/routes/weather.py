from fastapi import APIRouter, HTTPException, Depends, Query, status
from api.db.query import get_latest_data_query, get_latest_metrics_query
from api.db.config import get_db
from common.settings.config import app_settings
from api.db.schemas import CurrentWeatherSchema, ErrorDetails, WeatherMetricsResponse
from sqlalchemy.orm import Session
from middleware import cache

router = APIRouter(prefix="/v1")

@router.get("/weather", responses={
    200: {'model': CurrentWeatherSchema, 'description': 'Successful Request'},
    404: {'model': ErrorDetails, 'description': 'Unsuccessful Request'}
})
async def get_latest_data(
    lat: float = Query(ge=-90, le=90, description="Latitude of the location"),
    lon: float = Query(ge=-180, le=180, description="Longitude of the location"),
    db: Session =
    Depends(get_db)
) -> CurrentWeatherSchema:
    key = f"latest_weather_{lat}_{lon}"
    weather = await cache.get(key)
    if not weather:
        weather = get_latest_data_query(lat=lat, lon=lon, db=db)
        await cache.put(key, weather, ttl=5*60)
        if not weather:
            error_msg = {
                'status': status.HTTP_404_NOT_FOUND,
                'msg': "Data not found for given GPS coordinates",
                'result': "Some error message"
            }
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg)
    return weather


@router.get("/weather_metrics",
            responses={200: {'model': WeatherMetricsResponse,
                             'description': 'Successful Request'},
                       404: {'model': ErrorDetails,
                             'description': 'Unsuccessful Request'}})
async def get_latest_metrics(
    lat: float = Query(ge=-90, le=90, description="Latitude of the location"),
    lon: float = Query(ge=-180, le=180, description="Longitude of the location"),
    metrics: list[str] = Query(..., description="List of metrics to be retrieved", example=["wind", "temp"]),
    db: Session = Depends(get_db)
) -> WeatherMetricsResponse:
    
    if not metrics:
        raise HTTPException(status_code=400,
                            detail="At least one metric must be provided")

    key = f"latest_weather_metrics_{lat}_{lon}"
    obj = await cache.get(key)
    print(obj, 'from cache')
    if not obj:
        obj = get_latest_metrics_query(lat=lat, lon=lon, db=db, metrics=metrics)
        if "error" in obj:
            error_msg = {
                'status': status.HTTP_404_NOT_FOUND,
                'msg': obj['error'],
                'result': "Some error message"
            }
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg)
        # If user inputs wrong metrics, the coordinates will be cached
        # still
        await cache.put(key, obj, ttl=5*60)
    print(obj)
    return obj
