def normalize_api_resp(data: dict):
    location_obj = {
        'cityname': data['name'],
        'country': data['sys']['country'],
        'timezone': {'shift_seconds': data['timezone']},
        'sunrise': data['sys']['sunrise'],
        'sunset': data['sys']['sunset'],
        'longitude': round(data['coord']['lon'], ndigits=3),
        'latitude': round(data['coord']['lat'], ndigits=3)
    }

    volume_obj = {
        # Check existence of keys rain/snow and hours. If exists, return
        # values, else return None
        'rain_1h': data['rain']['1h'] if data.get('rain', {}).get('1h') else None,
        'rain_3h': data['rain']['3h'] if data.get('rain', {}).get('3h') else None,
        'snow_1h': data['snow']['1h'] if data.get('snow', {}).get('1h') else None,
        'snow_3h': data['snow']['3h'] if data.get('snow', {}).get('3h') else None
    }

    wind_obj = {
        'speed': data['wind']['speed'],
        'deg': data['wind'].get('deg', None),
        'gust': data['wind'].get('gust', None)
    }

    weather_metrics_obj = {
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'pressure': data['main']['pressure'],
        # some APIs might not always provide this
        'visibility': data.get('visibility', None),
        'cloudiness': data['clouds']['all'],
        'wind': wind_obj,
        'humidity': data['main']['humidity'],
        'temp_min': data['main']['temp_min'],
        'temp_max': data['main']['temp_max'],
        # sea level might not be provided
        'sea_level': data['main'].get('sea_level', None),
        # ground level might not be provided
        'grnd_level': data['main'].get('grnd_level', None)
    }

    current_weather = {
        'fetch_time': data['fetch_time'],
        'dt_calculation': data['dt'],
        'location': location_obj,
        'metrics': weather_metrics_obj,
        'volume': volume_obj,
        'weathers': []
    }

    weather_objects = []
    for weather in data['weather']:
        weather_obj = {
            'id': weather['id'],
            'main': weather['main'],
            'description': weather['description'],
            'icon': weather['icon'],
        }
        weather_objects.append(weather_obj)
    current_weather['weathers'] = weather_objects
    return current_weather
