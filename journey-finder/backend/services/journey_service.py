from typing import List
from datetime import timedelta
from ..models.journey import Journey
from ..models.flight_event import FlightEvent
from ..repositories.flight_api_client import FlightApiClient

class JourneyService:
    """
    Servicio que genera "viajes" a partir de eventos de vuelo.
    Permite hasta 2 eventos por viaje y aplica restricciones de duración y conexión.
    """

    def __init__(self, flight_api_client: FlightApiClient):
        self.client = flight_api_client

    async def search(self, date: str, from_code: str, to_code: str) -> List[Journey]:
        """
        Busca todos los viajes que cumplan las condiciones:
        - Fecha de salida igual a 'date'
        - Origen: from_code
        - Destino: to_code
        - Hasta 2 vuelos por viaje
        - Duración total ≤ 24h
        - Conexión entre vuelos ≤ 4h
        """
        from_code = from_code.upper()
        to_code = to_code.upper()

        # Traemos todos los eventos de vuelo
        all_events: List[FlightEvent] = await self.client.fetch_all_events()

        # Filtramos solo eventos que salen en la fecha indicada
        events_today = [e for e in all_events if e.departure_time.strftime("%Y-%m-%d") == date]

        journeys: List[Journey] = []

        # 1️⃣ Viajes directos
        for e in events_today:
            if e.from_ == from_code and e.to == to_code:
                journeys.append(Journey(connections=1, path=[e]))

        # 2️⃣ Viajes con 1 conexión
        for e1 in events_today:
            if e1.from_ != from_code:
                continue

            for e2 in events_today:
                # Conexión: el primer vuelo llega donde sale el segundo
                if e1.to != e2.from_:
                    continue
                if e2.to != to_code:
                    continue

                # Tiempo de conexión ≤ 4h
                connection_time = e2.departure_time - e1.arrival_time
                if connection_time < timedelta(0) or connection_time > timedelta(hours=4):
                    continue

                # Duración total ≤ 24h
                total_duration = e2.arrival_time - e1.departure_time
                if total_duration > timedelta(hours=24):
                    continue

                journeys.append(Journey(connections=2, path=[e1, e2]))

        return journeys
