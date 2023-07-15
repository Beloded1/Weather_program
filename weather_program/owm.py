
from datetime import date, datetime
from typing import List

import requests
from fastapi import HTTPException
from weather_program.schemas import Weather


class OpenweathermapClient:

    def __init__(self, api_key: str, url: str) -> None:
        self.api_key = api_key
        self.url = url

    def get_current_weather(self, city: str, units: str | None) -> Weather:
        url = f'{self.url}/weather'
        try:
            query = {'q': city, 'appid': self.api_key}
            if units:
                query['units'] = units
            response = requests.get(url, params=query)
            response.raise_for_status()
            data = response.json()
            return Weather(
                date=date.today(),
                temperature=data['main']['temp'],
                wind_speed=data.get('wind', {}).get('speed'),
                humidity=data.get('main', {}).get('humidity'),
            )
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_weather_forecast(self, city: str, units: str | None) -> List[Weather]:
        url = f'{self.url}/forecast'
        try:
            query = {'q': city, 'appid': self.api_key}
            if units:
                query['units'] = units
            response = requests.get(url, params=query)
            response.raise_for_status()
            data = response.json()

            forecast_data = data['list'][:40:8]

            forecast = []

            for item in forecast_data:
                date = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
                temperature = item['main']['temp']
                wind_speed = item['wind']['speed']
                humidity = item['main']['humidity']

                weather = Weather(
                    date=date,
                    temperature=temperature,
                    wind_speed=wind_speed,
                    humidity=humidity,
                )
                forecast.append(weather)

            return forecast

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=400, detail=str(e))
