from main import app
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test__current_weather__if_get_valid_city():
    response = client.get("/weather?city=Samara,RU")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data


def test__current_weather__if_get_invalid_city():
    response = client.get("/weather?city=InvalidCity")
    assert response.status_code == 400
