import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from types import SimpleNamespace

from backend.main import app

client = TestClient(app)

# Datos de ejemplo convertidos a objetos tipo FlightEvent
flight_events_data = [
    {"flight_number": "IB1234", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2024-10-19T08:00:00Z", "arrival_datetime": "2024-10-19T14:00:00Z"},
    {"flight_number": "IB2345", "departure_city": "BUE", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T16:00:00Z", "arrival_datetime": "2024-10-19T22:00:00Z"},
    {"flight_number": "IB3456", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T09:00:00Z", "arrival_datetime": "2024-10-19T18:00:00Z"},
    {"flight_number": "IB4567", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-19T11:00:00Z"},
    {"flight_number": "IB5678", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T12:30:00Z", "arrival_datetime": "2024-10-19T18:30:00Z"},
    {"flight_number": "IB6789", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-19T11:00:00Z"},
    {"flight_number": "IB7890", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T16:30:00Z", "arrival_datetime": "2024-10-19T22:30:00Z"},
    {"flight_number": "IB8901", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-20T06:00:00Z"},
    {"flight_number": "IB9012", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-20T06:30:00Z", "arrival_datetime": "2024-10-20T12:30:00Z"},

    # Cruzan medianoche
    {"flight_number": "VD1001", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-20T23:00:00Z", "arrival_datetime": "2024-10-21T01:00:00Z"},
    {"flight_number": "VC2001", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2024-10-20T21:00:00Z", "arrival_datetime": "2024-10-20T22:00:00Z"},
    {"flight_number": "VC2002", "departure_city": "BUE", "arrival_city": "NYC",
     "departure_datetime": "2024-10-20T23:00:00Z", "arrival_datetime": "2024-10-21T01:00:00Z"},
    {"flight_number": "VC3001", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2024-10-20T22:00:00Z", "arrival_datetime": "2024-10-20T23:00:00Z"},
    {"flight_number": "VC3002", "departure_city": "BUE", "arrival_city": "NYC",
     "departure_datetime": "2024-10-21T01:00:00Z", "arrival_datetime": "2024-10-21T02:00:00Z"},
]

# Convertir dict a objetos simples tipo FlightEvent que tu servicio espera
flight_events = [
    SimpleNamespace(
        flight_number=f["flight_number"],
        from_=f["departure_city"],
        to=f["arrival_city"],
        departure_time=f["departure_datetime"],
        arrival_time=f["arrival_datetime"]
    )
    for f in flight_events_data
]

@pytest.fixture(autouse=True)
def setup_flights(monkeypatch):
    # Sobreescribimos fetch_all_events del cliente de API
    from backend.repositories.flight_api_client import FlightApiClient

    async def mock_fetch_all_events(self):
        return flight_events

    monkeypatch.setattr(FlightApiClient, "fetch_all_events", mock_fetch_all_events)

# ----------------- TESTS -----------------

def test_direct_flight():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "MAD", "to": "BUE"})
    assert response.status_code == 200
    data = response.json()
    # Debe haber un vuelo directo
    assert any(j["connections"] == 1 and j["path"][0]["flight_number"] == "IB1234" for j in data)

def test_valid_connection():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "BUE", "to": "NYC"})
    data = response.json()
    # Debe incluir la conexión válida IB4567 + IB5678
    assert any(
        len(j["path"]) == 2 and
        j["path"][0]["flight_number"] == "IB4567" and
        j["path"][1]["flight_number"] == "IB5678"
        for j in data
    )

def test_connection_over_4h():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "BUE", "to": "NYC"})
    data = response.json()
    # La conexión con espera > 4h no debe aparecer
    assert not any(
        len(j["path"]) == 2 and
        j["path"][0]["flight_number"] == "IB6789" and
        j["path"][1]["flight_number"] == "IB7890"
        for j in data
    )

def test_total_duration_over_24h():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "BUE", "to": "NYC"})
    data = response.json()
    # Conexión con duración total > 24h no debe aparecer
    assert not any(
        len(j["path"]) == 2 and
        j["path"][0]["flight_number"] == "IB8901" and
        j["path"][1]["flight_number"] == "IB9012"
        for j in data
    )

def test_no_flights():
    response = client.get("/journeys/search", params={"date": "2024-10-22", "from": "MAD", "to": "BUE"})
    assert response.status_code == 200
    assert response.json() == []

def test_invalid_origin():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "NYC", "to": "BUE"})
    assert response.json() == []

def test_invalid_destination():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "MAD", "to": "PAR"})
    assert response.json() == []

def test_multiple_options():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "BUE", "to": "NYC"})
    data = response.json()
    flight_paths = [[f["flight_number"] for f in j["path"]] for j in data]
    assert ["IB2345"] in flight_paths  # directo
    assert ["IB4567", "IB5678"] in flight_paths  # conexión

def test_midnight_crossing():
    response = client.get("/journeys/search", params={"date": "2024-10-20", "from": "MAD", "to": "NYC"})
    data = response.json()
    # Debe incluir vuelos que cruzan medianoche
    assert any(
        j["path"][0]["flight_number"] == "VC2001" and j["path"][1]["flight_number"] == "VC2002"
        for j in data
    )
    # También vuelos directos que cruzan medianoche
    assert any(
        j["path"][0]["flight_number"] == "VD1001"
        for j in data if j["connections"] == 1
    )
