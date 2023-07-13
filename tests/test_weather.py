from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import OpenweathermapClient, Weather, app

client = TestClient(app)


def test__current_weather__if_get_invalid_city():
    response = client.get("/current_weather?city=InvalidCity")
    assert response.status_code == 400


def test__weather_forecast():
    response = client.get("/weather_forecast?city=Anapa")
    assert response.status_code == 200

    forecast_html = response.text
    assert "<h2>Weather forecast for Anapa</h2>" in forecast_html
    assert "<b>Date:</b>" in forecast_html
    assert "<b>Temperature:</b>" in forecast_html
    assert "<b>Wind Speed:</b>" in forecast_html
    assert "<b>Humidity:</b>" in forecast_html


@patch.object(OpenweathermapClient, 'get_weather_forecast')
def test__weather_forecast__with_mock(mock_get_weather_forecast):
    mock_get_weather_forecast.return_value = [
        Weather(
            date=datetime(2023, 7, 14),
            temperature=24.5,
            wind_speed=4.2,
            humidity=60
        ),
        Weather(
            date=datetime(2023, 7, 15),
            temperature=23.8,
            wind_speed=3.8,
            humidity=55
        )
    ]

    response = client.get("/weather_forecast?city=Anapa")
    assert response.status_code == 200

    forecast_html = response.text
    assert "<h2>Weather forecast for Anapa</h2>" in forecast_html
    assert "<b>Date:</b> 2023-07-14" in forecast_html
    assert "<b>Temperature:</b> 24.5°C" in forecast_html
    assert "<b>Wind Speed:</b> 4.2 m/s" in forecast_html
    assert "<b>Humidity:</b> 60%" in forecast_html
    assert "<b>Date:</b> 2023-07-15" in forecast_html
    assert "<b>Temperature:</b> 23.8°C" in forecast_html
    assert "<b>Wind Speed:</b> 3.8 m/s" in forecast_html
    assert "<b>Humidity:</b> 55%" in forecast_html



