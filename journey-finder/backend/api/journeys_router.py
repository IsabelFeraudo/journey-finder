"""Router que expone el endpoint /journeys/search.
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

router = APIRouter(tags=["Journeys"])


# URL base de la API mock local
FLIGHT_API_BASE_URL = "http://127.0.0.1:8001"


async def get_journey_service() -> JourneyService:
    """ Patron Factory. Creamos el JourneyService con la implementación concreta del cliente.
    Eventualmente se modificaria para inyectar la API real de vuelos """
    client = FlightApiClient(base_url=FLIGHT_API_BASE_URL)
    service = JourneyService(flight_api_client=client)
    return service


@router.get("/search", response_model=List[Journey])
async def search_journeys(
    date: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$", description="Fecha de salida en formato YYYY-MM-DD"),
    from_: str = Query(..., alias="from", min_length=3, max_length=3, description="Código IATA del aeropuerto de origen"),
    to: str = Query(..., min_length=3, max_length=3, description="Código IATA del aeropuerto de destino"),
    service: JourneyService = Depends(get_journey_service)
):
    """Endpoint GET /journeys/search?date=YYYY-MM-DD&from=BUE&to=MAD
    - Valida inputs vía Query parameters
    - Llama al JourneyService.search(), que internamente consume el endpoint local `/flight-events`
    - Devuelve una lista de journeys que coincidan con los filtros"""
    try:
        results = await service.search(date=date, from_code=from_, to_code=to)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar viajes: {str(e)}")
