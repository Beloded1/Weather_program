from datetime import date, datetime

from pydantic import BaseModel


class Weather(BaseModel):
    date: datetime | date
    temperature: float
    wind_speed: None | float
    humidity: None | int
