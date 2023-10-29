def extract_wind_data(weather_metrics):
    return {
        "speed": weather_metrics.wind.speed,
        "deg": weather_metrics.wind.deg,
        "gust": weather_metrics.wind.gust
    }


def extract_temp_data(weather_metrics):
    return weather_metrics.temp


METRIC_EXTRACTION_MAP = {
    "wind": extract_wind_data,
    "temp": extract_temp_data
}
