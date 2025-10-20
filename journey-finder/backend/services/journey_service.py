from typing import List
from datetime import timedelta, datetime
from ..models.journey import Journey
from ..models.flight_event import FlightEvent
from ..repositories.flight_api_client import FlightApiClient

class JourneyService:
    """Servicio que genera Journeys a partir de eventos de vuelo FlightEvents.
    Permite hasta 2 vuelos por viaje:
    -Vuelos directos (sin conexiones)
    -Vuelos con 1 conexión (2 tramos)

    Reglas de negocio:
    -Fecha de salida = fecha solicitada
    -Duración total ≤ 24 horas
    -Conexión entre vuelos ≤ 4 horas"""

    def __init__(self, flight_api_client: FlightApiClient):
        self.client = flight_api_client

    @staticmethod
    def parse_datetime(dt_str: str) -> datetime:
        """Convierte string ISO con Z a datetime UTC"""
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

    async def search(self, date: str, from_code: str, to_code: str) -> List[Journey]:
        from_code = from_code.upper()
        to_code = to_code.upper()

        all_events: List[FlightEvent] = await self.client.fetch_all_events()

        # Convertir fechas a datetime para todos los vuelos
        parsed_events = []
        for e in all_events:
            departure_dt = self.parse_datetime(e.departure_time) if isinstance(e.departure_time, str) else e.departure_time
            arrival_dt = self.parse_datetime(e.arrival_time) if isinstance(e.arrival_time, str) else e.arrival_time
            parsed_events.append((e, departure_dt, arrival_dt))

        # Filtrar vuelos que salen en la fecha solicitada
        events_today = [(e, dep, arr) for e, dep, arr in parsed_events if dep.date().isoformat() == date]

        journeys: List[Journey] = []

        #Vuelos directos
        for e, dep, arr in events_today:
            if e.from_ == from_code and e.to == to_code:
                journeys.append(Journey.from_flights([e]))

        #Vuelos con conexión
        for e1, dep1, arr1 in events_today:
            if e1.from_ != from_code:
                continue

            for e2, dep2, arr2 in parsed_events:  # permitimos segundo vuelo de otra fecha
                if e1.to != e2.from_ or e2.to != to_code:
                    continue

                connection_time = dep2 - arr1
                if connection_time < timedelta(0) or connection_time > timedelta(hours=4):
                    continue

                total_duration = arr2 - dep1
                if total_duration > timedelta(hours=24):
                    continue

                journeys.append(Journey.from_flights([e1, e2]))

        return journeys
