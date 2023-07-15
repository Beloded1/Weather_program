from datetime import date

from fastapi.testclient import TestClient
from weather_program.schemas import Weather
from weather_program.server import app

client = TestClient(app)


def test__current_weather__if_get_invalid_city():
    response = client.get("/current_weather?city=InvalidCity")
    assert response.status_code == 400


def test_weather_forecast_error():
    response = client.get("/weather_forecast")
    assert response.status_code == 422

    error_detail = response.json()['detail']
    assert error_detail[0]['msg'] == "Field required"


def test__weather_forecast():
    response = client.get("/weather_forecast?city=Anapa")
    assert response.status_code == 200

    data = response.json()
    assert "city" in data
    assert "forecast" in data
    assert isinstance(data["forecast"], list)
    assert len(data["forecast"]) > 0

    forecast_entry = data["forecast"][0]
    assert "date" in forecast_entry
    assert "temperature" in forecast_entry
    assert "wind_speed" in forecast_entry
    assert "humidity" in forecast_entry


def test__current_weather__with_mock(mock_ovm_client):
    mock_weather = Weather(
        date=date(2022, 1, 1),
        temperature=25.0,
        wind_speed=5.0,
        humidity=70
    )
    mock_ovm_client.get_current_weather.return_value = mock_weather

    client = TestClient(app)
    response = client.get("/current_weather?city=Anapa")

    assert response.status_code == 200
    weather = response.json()
    assert weather == {
        'date': '2022-01-01',
        'temperature': 25.0,
        'wind_speed': 5.0,
        'humidity': 70
    }

def test__weather_forecast__with_mock(mock_ovm_client):
    mock_forecast = [
        Weather(
            date=date(2022, 1, 1),
            temperature=25.0,
            wind_speed=5.0,
            humidity=70
        ),
        Weather(
            date=date(2022, 1, 2),
            temperature=23.0,
            wind_speed=4.0,
            humidity=65
        ),
    ]
    mock_ovm_client.get_weather_forecast.return_value = mock_forecast

    client = TestClient(app)
    response = client.get("/weather_forecast?city=Anapa")

    assert response.status_code == 200
    forecast = response.json()
    assert forecast == {
        'city': 'Anapa',
        'forecast': [
            {
                'date': '2022-01-01',
                'temperature': 25.0,
                'wind_speed': 5.0,
                'humidity': 70
            },
            {
                'date': '2022-01-02',
                'temperature': 23.0,
                'wind_speed': 4.0,
                'humidity': 65
            },
        ]
    }

