import requests
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
from fastapi import HTTPException


app = FastAPI()
load_dotenv()


class Weather(BaseModel):
    city: str
    temperature: float


@app.get("/weather")
def current_weather(
    city: str = Query("Samara,RU", description="City name"),
    units: Optional[str] = Query("metric", description="Temperature units"),
):
    api_key = os.environ['MYAPP_OPEN_WEATHER_KEY']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        temperature = data['main']['temp']
        weather_data = Weather(city=city, temperature=temperature)
        return weather_data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e)) 