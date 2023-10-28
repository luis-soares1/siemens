from fastapi import APIRouter, HTTPException, Depends
from api.db.config import get_db, get_settings
from sqlalchemy.orm import Session
from middleware import cache

router = APIRouter()
settings= get_settings()

@router.post("/receive_data/weather")
async def receive_latest_data(data: dict, db: Session = Depends(get_db)):
    print('received!')
    # try:
    #     db.add(data)
    #     db.commit()
    #     db.refresh(data)
    #     return {"Status: OK"}
    # except:
    #     db.rollback()
    #     HTTPException(status_code=422, detail="Invalid data format. Call the backend dev.")
    # finally:
    #     db.close()
        
# async def save_weather_data_to_db(db, data: dict) -> None:
#     timestamp_fetched = datetime.now()

#     location_obj = create_location(db, {
#         'cityname': data['name'],
#         'country': data['sys']['country'],
#         'timezone_id': create_timezone(db, {'shift_seconds': data['timezone']}).id,
#         'sunrise': data['sys']['sunrise'],
#         'sunset': data['sys']['sunset'],
#         'longitude': round(data['coord']['lon'], ndigits=3),
#         'latitude': round(data['coord']['lat'], ndigits=3)
#     })

#     volume_obj = create_volumes(db, {
#         # Check existence of keys rain/snow and hours. If exists, return
#         # values, else return None
#         'rain_1h': data['rain']['1h'] if data.get('rain', {}).get('1h') else None,
#         'rain_3h': data['rain']['3h'] if data.get('rain', {}).get('3h') else None,
#         'snow_1h': data['snow']['1h'] if data.get('snow', {}).get('1h') else None,
#         'snow_3h': data['snow']['3h'] if data.get('snow', {}).get('3h') else None
#     })

#     wind_obj = create_wind(db, {
#         'speed': data['wind']['speed'],
#         'deg': data['wind'].get('deg', None),
#         'gust': data['wind'].get('gust', None)
#     })

#     weather_metrics_obj = create_weather_metrics(db, {
#         'temp': data['main']['temp'],
#         'feels_like': data['main']['feels_like'],
#         'pressure': data['main']['pressure'],
#         # some APIs might not always provide this
#         'visibility': data.get('visibility', None),
#         'cloudiness': data['clouds']['all'],
#         'wind_id': wind_obj.id,
#         'humidity': data['main']['humidity'],
#         'temp_min': data['main']['temp_min'],
#         'temp_max': data['main']['temp_max'],
#         # sea level might not be provided
#         'sea_level': data['main'].get('sea_level', None),
#         # ground level might not be provided
#         'grnd_level': data['main'].get('grnd_level', None)
#     })

#     current_weather = create_current_weather(db, {
#         'fetch_time': timestamp_fetched,
#         'dt_calculation': data['dt'],
#         'location_id': location_obj.id,
#         'weather_metrics_id': weather_metrics_obj.id,
#         'volume_id': volume_obj.id
#     })


#     weather_objects = []
#     for weather in data['weather']:
#         weather_obj = create_weather(db, {
#             'id': weather['id'],
#             'main': weather['main'],
#             'description': weather['description'],
#             'icon': weather['icon'],
#         })
#         weather_objects.append(weather_obj)

#     current_weather.weathers = weather_objects
#     db.commit()
#     db.refresh(current_weather)
