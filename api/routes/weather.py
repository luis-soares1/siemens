from fastapi import APIRouter, HTTPException, Depends, Query
from db.query import get_latest_data_query, get_latest_metrics_query
from db.config import get_db, get_settings
from sqlalchemy.orm import Session
from middleware import cache

router = APIRouter(prefix="/v1")
settings = get_settings()


@router.get("/weather")
async def get_latest_data(lat: float, lon: float, db: Session = Depends(get_db)):
    key = f"latest_weather_{lat}_{lon}"
    # weather = await cache.get(key)
    # if not weather:
    weather = get_latest_data_query(lat=lat, lon=lon, db=db)
    # await cache.put(key, weather, settings.job_interval)
    if not weather:
        raise HTTPException(
            status_code=404,
            detail="Data not found for given GPS coordinates")
    print(weather.location)
    return weather


def validate_metrics(metrics: list[str]) -> list[str]:
    if not metrics or len(metrics) == 0:
        raise HTTPException(status_code=400,
                            detail="At least one metric must be provided")
    return metrics


@router.get("/weather_metrics")
async def get_latest_metrics(
    lat: float = Query(..., description="Latitude of the location"),
    lon: float = Query(..., description="Longitude of the location"),
    metrics: list[str] = Query(..., description="List of metrics to be retrieved", example=["wind", "temp"]),
    db: Session = Depends(get_db)
):
    metrics = validate_metrics(metrics)

    key = f"latest_weather_metrics_{lat}_{lon}"
    # obj = await cache.get(key)
    # if not obj:
    obj = get_latest_metrics_query(lat=lat, lon=lon, db=db, metrics=metrics)
    # await cache.put(key, obj, settings.job_interval)
    if "error" in obj:
        raise HTTPException(status_code=404, detail=obj['error'])

    return obj
