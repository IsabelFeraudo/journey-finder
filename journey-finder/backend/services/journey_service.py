from typing import List
from datetime import timedelta
from ..models.journey import Journey
from ..models.flight_event import FlightEvent
from ..repositories.flight_api_client import FlightApiClient

class JourneyService:
    """
    Servicio que genera "viajes" (Journeys) a partir de eventos de vuelo (FlightEvents).

    Permite hasta 2 vuelos por viaje:
    - Vuelos directos (0 conexiones)
    - Vuelos con 1 conexión (2 tramos)

    Reglas:
    - Fecha de salida = fecha solicitada.
    - Duración total ≤ 24 horas.
    - Conexión entre vuelos ≤ 4 horas.
    """

    def __init__(self, flight_api_client: FlightApiClient):
        # Inyección del cliente de API que obtiene los eventos
        self.client = flight_api_client

    async def search(self, date: str, from_code: str, to_code: str) -> List[Journey]:
        """
        Busca todos los posibles viajes que cumplan las condiciones.

        Parámetros:
        - date: fecha de salida (YYYY-MM-DD)
        - from_code: código IATA de origen (ej: "MAD")
        - to_code: código IATA de destino (ej: "BUE")

        Retorna:
        - Lista de objetos Journey (directos o con una conexión)
        """
        from_code = from_code.upper()
        to_code = to_code.upper()

        # 🔹 1. Obtener todos los eventos de vuelo
        all_events: List[FlightEvent] = await self.client.fetch_all_events()

        # 🔹 2. Filtrar solo los vuelos que salen en la fecha indicada
        events_today = [
            e for e in all_events
            if e.departure_time.strftime("%Y-%m-%d") == date
        ]

        journeys: List[Journey] = []

        # 🔹 3. Viajes directos (sin conexión)
        for e in events_today:
            if e.from_ == from_code and e.to == to_code:
                journeys.append(Journey.from_flights([e]))

        # 🔹 4. Viajes con una conexión (2 vuelos)
        for e1 in events_today:
            if e1.from_ != from_code:
                continue

            for e2 in events_today:
                # Debe conectar correctamente
                if e1.to != e2.from_:
                    continue
                if e2.to != to_code:
                    continue

                # Tiempo entre vuelos ≤ 4h
                connection_time = e2.departure_time - e1.arrival_time
                if connection_time < timedelta(0) or connection_time > timedelta(hours=4):
                    continue

                # Duración total ≤ 24h
                total_duration = e2.arrival_time - e1.departure_time
                if total_duration > timedelta(hours=24):
                    continue

                journeys.append(Journey.from_flights([e1, e2]))

       
        return journeys
