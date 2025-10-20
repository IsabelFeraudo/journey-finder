from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/flight-events")
async def get_flight_events():
    """
    Mock API que retorna una lista fija de vuelos disponibles.
    Simula el comportamiento de la API externa.
    """
    return [
        {
            "flight_number": "IB1234",
            "departure_city": "MAD",
            "arrival_city": "BUE",
            "departure_datetime": "2021-12-31T23:59:59.000Z",
            "arrival_datetime": "2022-01-01T08:00:00.000Z"
        },
        {
            "flight_number": "AF5678",
            "departure_city": "MAD",
            "arrival_city": "CDG",
            "departure_datetime": "2021-12-31T20:00:00.000Z",
            "arrival_datetime": "2021-12-31T22:00:00.000Z"
        },
        {
            "flight_number": "AF9012",
            "departure_city": "CDG",
            "arrival_city": "BUE",
            "departure_datetime": "2021-12-31T23:00:00.000Z",
            "arrival_datetime": "2022-01-01T08:00:00.000Z"
        }
    ]
