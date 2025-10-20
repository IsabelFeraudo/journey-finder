"""Modelo Journey: representa un viaje completo (1 o 2 eventos de vuelo).
Principios SOLID Implementados:
- Single Responsibility: clase representa un viaje con sus conexiones.
- Open/Closed: extensible para agregar mas validaciones o propiedades."""

from pydantic import BaseModel
from typing import List
from .flight_event import FlightEvent

class Journey(BaseModel):
    """ Representa un viaje completo (directo o con una o mas conexiones).
    Atributos:
    - connections: cantidad de conexiones
    - path: lista de FlightEvent que componen el viaje"""

    connections: int
    path: List[FlightEvent]

    @classmethod
    def from_flights(cls, flights: List[FlightEvent]) -> "Journey":
        """Crea un Journey a partir de una lista de vuelos.
        Calcula  la cantidad de conexiones."""
        return cls(
            connections=len(flights) - 1,
            path=flights
        )
