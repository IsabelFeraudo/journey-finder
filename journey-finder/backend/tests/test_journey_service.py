"""
Tests unitarios e integración ligera del JourneyService.
Usamos respx para mockear llamadas HTTP del httpx AsyncClient.
"""

import pytest
from httpx import AsyncClient
import respx
from datetime import datetime
from ..repositories.flight_api_client import FlightApiClient
from ..services.journey_service import JourneyService
from ..models.flight_event import FlightEvent
import asyncio

@pytest.mark.asyncio
async def test_direct_and_connected_journeys():
    # Mock: creamos una respuesta simulada de la API de eventos
    mocked_payload = [
        {
            "flight_number": "XX1234",
            "from": "BUE",
            "to": "MAD",
            "departure_time": "2024-09-12T12:00:00",
            "arrival_time": "2024-09-13T00:00:00"
        },
        {
            "flight_number": "XX2345",
            "from": "MAD",
            "to": "PMI",
            "departure_time": "2024-09-13T02:00:00",
            "arrival_time": "2024-09-13T03:00:00"
        },
        # vuelo no relacionado
        {
            "flight_number": "YY9999",
            "from": "BUE",
            "to": "LON",
            "departure_time": "2024-09-12T10:00:00",
            "arrival_time": "2024-09-12T18:00:00"
        }
    ]

    async with respx.mock(assert_all_called=False) as mock:
        mock.get("https://events-api.example.com/events").respond(json=mocked_payload)

        client = FlightApiClient(base_url="https://events-api.example.com")
        svc = JourneyService(flight_api_client=client)

        results = await svc.search(date="2024-09-12", from_code="BUE", to_code="PMI")
        # Debe encontrar el viaje BUE->MAD + MAD->PMI
        # y posiblemente directos si existieran (no en este payload)
        assert any(j.connections == 2 for j in results)
        # Verificamos datos de la ruta
        found = False
        for j in results:
            if j.connections == 2:
                assert j.path[0].flight_number == "XX1234"
                assert j.path[1].flight_number == "XX2345"
                found = True
        assert found
