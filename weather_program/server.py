import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Query
from weather_program.config import Config
from weather_program.owm import OpenweathermapClient
from weather_program.schemas import Weather

app = FastAPI()
config = Config(api_key=os.environ['MYAPP_OPEN_WEATHER_KEY'])
ovm_client = OpenweathermapClient(
    api_key=config.api_key,
    url='http://api.openweathermap.org/data/2.5',
)


@app.get('/current_weather')
def current_weather(
    city: str = Query(description='City name'),
    units: None | str = Query('metric', description='Units'),
) -> Weather:
    return ovm_client.get_current_weather(city, units)


@app.get('/weather_forecast', response_model=Dict[str, Any])
def weather_forecast(
    city: str = Query(description='City name'),
    units: None | str = Query('metric', description='Units'),
) -> Dict[str, Any]:
    try:
        forecast_data = ovm_client.get_weather_forecast(city, units)

        forecast_json: Dict[str, Any] = {
            'city': city,
            'forecast': [],
        }

        for item in forecast_data:
            forecast_entry: Dict[str, Any] = {
                'date': item.date,
                'temperature': item.temperature,
                'wind_speed': item.wind_speed,
                'humidity': item.humidity,
            }
            forecast_json['forecast'].append(forecast_entry)

        return forecast_json

    except HTTPException as e:
        raise e
