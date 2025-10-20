"""
Modelo Journey: representa un viaje completo (1 o 2 eventos de vuelo).
Usamos Pydantic para validación y serialización.

Principios:
- Single Responsibility: clase representa un viaje con sus conexiones.
- Open/Closed: extensible para agregar más validaciones o propiedades.
"""
from pydantic import BaseModel
from typing import List
from .flight_event import FlightEvent

class Journey(BaseModel):
    """
    Representa un viaje completo (directo o con una o más conexiones).

    Atributos:
    - connections: cantidad de conexiones (número de vuelos - 1)
    - path: lista de FlightEvent que componen el viaje
    """

    connections: int
    path: List[FlightEvent]

    @classmethod
    def from_flights(cls, flights: List[FlightEvent]) -> "Journey":
        """
        Crea un Journey a partir de una lista de vuelos.
        Calcula automáticamente la cantidad de conexiones.

        Ejemplo:
        - [vuelo1] → 0 conexiones (directo)
        - [vuelo1, vuelo2] → 1 conexión
        """
        return cls(
            connections=len(flights) - 1,
            path=flights
        )
