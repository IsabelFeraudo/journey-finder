"""
Router que expone el endpoint /journeys/search.
Aquí aplicamos la capa de presentación (controller) que recibe parámetros HTTP y delega al servicio.

Principios:
- Single Responsibility: el router sólo valida input y delega.
- Dependency Inversion: el servicio inyecta un cliente concreto si corresponde.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from ..models.journey import Journey
from ..repositories.flight_api_client import FlightApiClient
from ..services.journey_service import JourneyService

router = APIRouter()

# CONFIG: URL base de la API de eventos (sin /flight-events al final)
FLIGHT_API_BASE_URL = "http://127.0.0.1:8000"

async def get_journey_service():
    """
    Factory que crea el JourneyService con la implementación concreta del cliente.
    En producción podrías inyectar una implementación distinta.
    """
    client = FlightApiClient(base_url=FLIGHT_API_BASE_URL)
    service = JourneyService(flight_api_client=client)
    return service

@router.get("/search", response_model=List[Journey])
async def search_journeys(
    date: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$"),
    from_: str = Query(..., alias="from", min_length=3, max_length=3),
    to: str = Query(..., min_length=3, max_length=3),
    service: JourneyService = Depends(get_journey_service)
):
    """
    Endpoint GET /journeys/search?date=YYYY-MM-DD&from=BUE&to=MAD
    - Valida inputs vía Query parameters.
    - Llama al JourneyService.search y retorna la lista de journeys.
    - Ahora soporta vuelos directos y con 1 conexión, usando fetch_all_events.
    """
    try:
        results = await service.search(date=date, from_code=from_, to_code=to)
        return results
    except Exception as e:
        # En producción mejorar el manejo de errores y logging
        raise HTTPException(status_code=500, detail=str(e))
