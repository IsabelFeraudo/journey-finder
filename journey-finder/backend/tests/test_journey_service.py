import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from backend.main import app

client = TestClient(app)

# Datos de ejemplo
flight_events = [
    # Viaje directo 1 vuelo valido
    {"flight_number": "IB1234", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2024-10-19T08:00:00Z", "arrival_datetime": "2024-10-19T14:00:00Z"},

    # Viaje directo 1 vuelo valido
    {"flight_number": "IB2345", "departure_city": "BUE", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T16:00:00Z", "arrival_datetime": "2024-10-19T22:00:00Z"},

    # Viaje directo 1 vuelo
    {"flight_number": "IB3456", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T09:00:00Z", "arrival_datetime": "2024-10-19T18:00:00Z"},

    # Conexion valida (BUE -> MAD -> NYC)
    {"flight_number": "IB4567", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-19T11:00:00Z"},
    {"flight_number": "IB5678", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T12:30:00Z", "arrival_datetime": "2024-10-19T18:30:00Z"},

    # Conexión invalida (espera > 4h)
    {"flight_number": "IB6789", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-19T11:00:00Z"},
    {"flight_number": "IB7890", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T16:30:00Z", "arrival_datetime": "2024-10-19T22:30:00Z"},

    # Conexión invalida (duración total > 24h)
    {"flight_number": "IB8901", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-20T06:00:00Z"},
    {"flight_number": "IB9012", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-20T06:30:00Z", "arrival_datetime": "2024-10-20T12:30:00Z"},

    # Vuelo pasando medianoche
    {"flight_number": "IB1231", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2021-12-31T23:59:59.000Z", "arrival_datetime": "2022-01-01T00:00:00.000Z"},
]


@pytest.fixture(autouse=True)
def setup_flights(monkeypatch):
    from backend.api.journeys_router import get_flight_events
    monkeypatch.setattr("backend.api.journeys_router.get_flight_events", lambda date: flight_events)

# ----------------- TESTS -----------------

def test_direct_flight():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "MAD", "to": "BUE"})
    assert response.status_code == 200
    data = response.json()
    assert any(j["connections"] == 1 for j in data)

def test_valid_connection():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "BUE", "to": "NYC"})
    data = response.json()
    assert any(
        len(j["path"]) == 2 and
        j["path"][0]["flight_number"] == "IB4567" and
        j["path"][1]["flight_number"] == "IB5678"
        for j in data
    )

def test_connection_over_4h():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "BUE", "to": "NYC"})
    data = response.json()
    assert not any(
        len(j["path"]) == 2 and
        j["path"][0]["flight_number"] == "IB6789" and
        j["path"][1]["flight_number"] == "IB7890"
        for j in data
    )

def test_total_duration_over_24h():
    response = client.get("/journeys/search", params={"date": "2024-10-19", "from": "BUE", "to": "NYC"})
    data = response.json()
    assert not any(
        len(j["path"]) == 2 and
        j["path"][0]["flight_number"] == "IB8901" and
        j["path"][1]["flight_number"] == "IB9012"
        for j in data
    )

def test_no_flights():
    response = client.get("/journeys/search", params={"date": "2024-10-20", "from": "MAD", "to": "BUE"})
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
    assert ["IB2345"] in flight_paths
    assert ["IB4567", "IB5678"] in flight_paths

def test_midnight_crossing():
    response = client.get("/journeys/search", params={"date": "2021-12-31", "from": "MAD", "to": "BUE"})
    data = response.json()
    assert any(f["flight_number"] == "IB1231" for j in data for f in j["path"])
