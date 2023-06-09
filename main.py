import requests
from fastapi import FastAPI


app = FastAPI()

@app.get("/items/{item_id}")
def current_weather():
    city = 'Samara,RU'
    api_key = '17c8ecf5f173d05e68f31b64cc7b5345'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    weather_data = {
        'city': city,
        'temperature': temperature,
    }

    return weather_data
