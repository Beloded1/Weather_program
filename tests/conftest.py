from unittest.mock import Mock

import pytest
from weather_program.schemas import OpenweathermapClient

@pytest.fixture
def mock_ovm_client(monkeypatch):
    mock_client = Mock(spec=OpenweathermapClient)
    monkeypatch.setattr("weather_program.server.ovm_client", mock_client)
    return mock_client
