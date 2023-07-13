import os
from datetime import date, datetime

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()
load_dotenv()


class Weather(BaseModel):
    date: datetime | date
    temperature: float
    wind_speed: None | float
    humidity: None | int


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

    def get_weather_forecast(self, city: str, units: str | None) -> list[Weather]:  
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
                date = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
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


ovm_client = OpenweathermapClient(
    api_key=os.environ['MYAPP_OPEN_WEATHER_KEY'],
    url="http://api.openweathermap.org/data/2.5",
)


@app.get("/current_weather")
def current_weather(
    city: str = Query(description="City name"),
    units: None | str = Query("metric", description="Units"),
) -> Weather:
    return ovm_client.get_current_weather(city, units)


@app.get("/weather_forecast", response_class=HTMLResponse)
def weather_forecast(
    city: str = Query(description="City name"),
    units: None | str = Query("metric", description="Units"),
) -> str:
    try:
        forecast_data = ovm_client.get_weather_forecast(city, units)

        forecast_html = f"<h2>Weather forecast for {city}</h2><br>"

        for item in forecast_data:
            forecast_html += f"<b>Date:</b> {item.date}<br>"
            forecast_html += f"<b>Temperature:</b> {item.temperature}°C<br>"
            forecast_html += f"<b>Wind Speed:</b> {item.wind_speed} m/s<br>"
            forecast_html += f"<b>Humidity:</b> {item.humidity}%<br><br>"

        return forecast_html

    except HTTPException as e:
        raise e


# # def 
#         plt.plot(dates, temperatures, label='Temperature')
#         plt.plot(dates, wind_speeds, label='Wind Speed')
#         plt.plot(dates, humidities, label='Humidity')
#         plt.xlabel('Date')
#         plt.ylabel('Value')
#         plt.title(f'Weather Forecast for {city}')
#         plt.xticks(rotation=45)
#         plt.legend()
#         plt.show()

#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=400, detail=str(e))

    