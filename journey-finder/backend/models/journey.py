"""
Modelo Journey: representa un viaje completo (1 o 2 eventos de vuelo).
Usamos Pydantic para validación y serialización.

Principios:
- Single Responsibility: clase representa un viaje con sus conexiones.
- Open/Closed: extensible para agregar más validaciones o propiedades.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List
from .flight_event import FlightEvent

class Journey(BaseModel):
    """
    Representa un 'journey' (viaje) que puede ser:
      - Directo: 1 conexión (un solo vuelo)
      - Con escala: 2 conexiones (dos vuelos)
    
    Campos:
      - connections: número de conexiones (1 o 2)
      - path: lista de eventos de vuelo que forman el viaje
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "connections": 1,
                "path": [
                    {
                        "flight_number": "AA123",
                        "from_": "BUE",
                        "to": "MAD",
                        "departure_time": "2024-01-15T10:00:00Z",
                        "arrival_time": "2024-01-15T22:00:00Z"
                    }
                ]
            }
        }
    )
    
    connections: int = Field(..., ge=1, le=2, description="Number of flight connections (1 or 2)")
    path: List[FlightEvent] = Field(..., min_length=1, max_length=2, description="List of flight events in the journey")

