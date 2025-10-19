"""
Repository (Repository Pattern) que encapsula acceso a la API externa de eventos de vuelo.
Aplicación del principio Dependency Inversion: el servicio dependerá de esta abstracción.
"""

from abc import ABC, abstractmethod
from typing import List
from ..models.flight_event import FlightEvent
import httpx
from datetime import datetime

class IFlightApiClient(ABC):
    """Interfaz para el cliente de la API de eventos de vuelo."""

    @abstractmethod
    async def fetch_events_for_date(self, date: str) -> List[FlightEvent]:
        """Obtiene todos los eventos de vuelo para una fecha en formato YYYY-MM-DD."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_all_events(self) -> List[FlightEvent]:
        """Obtiene todos los eventos de vuelo disponibles (sin filtrar por fecha)."""
        raise NotImplementedError


class FlightApiClient(IFlightApiClient):
    """
    Implementación concreta del cliente usando httpx.
    Responsabilidad única: obtener y mapear datos desde la API externa.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(timeout=10.0)

    async def fetch_events_for_date(self, date: str) -> List[FlightEvent]:
        """
        Llama a la API externa para obtener eventos de la fecha indicada.
        - date: YYYY-MM-DD
        """
        url = f"{self.base_url}/flight-events"
        resp = await self._client.get(url)
        resp.raise_for_status()
        payload = resp.json()

        events = []
        for item in payload:
            dep_time = datetime.fromisoformat(item["departure_datetime"].replace("Z", "+00:00"))
            arr_time = datetime.fromisoformat(item["arrival_datetime"].replace("Z", "+00:00"))

            # Filtramos solo los que coinciden con la fecha de salida
            if dep_time.strftime("%Y-%m-%d") == date:
                fe = FlightEvent(
                    flight_number=item["flight_number"],
                    from_=item["departure_city"],
                    to=item["arrival_city"],
                    departure_time=dep_time,
                    arrival_time=arr_time
                )
                events.append(fe)
        return events

    async def fetch_all_events(self) -> List[FlightEvent]:
        """
        Obtiene todos los eventos de vuelo disponibles sin filtrar por fecha.
        """
        url = f"{self.base_url}/flight-events"
        resp = await self._client.get(url)
        resp.raise_for_status()
        payload = resp.json()

        events = []
        for item in payload:
            dep_time = datetime.fromisoformat(item["departure_datetime"].replace("Z", "+00:00"))
            arr_time = datetime.fromisoformat(item["arrival_datetime"].replace("Z", "+00:00"))

            fe = FlightEvent(
                flight_number=item["flight_number"],
                from_=item["departure_city"],
                to=item["arrival_city"],
                departure_time=dep_time,
                arrival_time=arr_time
            )
            events.append(fe)
        return events
