"""Modelos del dominio: FlightEvent
Principios SOLID implementados:
- Single Responsibility: Esta clase tiene sólo propiedades de un evento de vuelo.
- Open/Closed: si agregamos nuevas validaciones, se extiende sin modificar consumidores..."""

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FlightEvent(BaseModel):
    """Representa un evento de vuelo, es decir una instancia de un vuelo en vuna fecha concreta
    Campos:
      - flight_number: número de vuelo (str)
      - from_: código de origen (str)
      - to: código de destino (str)
      - departure_time: datetime UTC de salida
      - arrival_time: datetime UTC de llegada"""
    
    model_config = ConfigDict()

    flight_number: str
    from_: str
    to: str
    departure_time: datetime
    arrival_time: datetime

    def duration_seconds(self) -> int:
        """Retorna la duración del evento en segundos.
        Principio: Single Responsibility. Calcula su duración """
        return int((self.arrival_time - self.departure_time).total_seconds())
