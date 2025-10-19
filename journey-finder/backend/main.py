"""
Main entrypoint for the backend FastAPI app.
Configura el app y registra routers.

Patrones/principios aplicados:
- Dependency Injection (D por Dependency Inversion)
- Single Responsibility: este módulo sólo configura la app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.journeys_router import router as journeys_router

app = FastAPI(title="Toy Flight Events API")
# Registramos el router con el prefijo /journeys
app.include_router(journeys_router, prefix="/journeys")
#Aca permitimos llamadas desde cualquier origen como por ej. un frontend, Postman o algun navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos de ejemplo para probar la logica de la API
flight_events = [
    {
        "flight_number": "IB1234",
        "departure_city": "MAD",
        "arrival_city": "BUE",
        "departure_datetime": "2024-10-19T08:00:00Z",
        "arrival_datetime": "2024-10-19T14:00:00Z"
    },
    {
        "flight_number": "IB2345",
        "departure_city": "BUE",
        "arrival_city": "LON",
        "departure_datetime": "2024-10-19T16:00:00Z",
        "arrival_datetime": "2024-10-19T22:00:00Z"
    },
    {
        "flight_number": "IB3456",
        "departure_city": "MAD",
        "arrival_city": "LON",
        "departure_datetime": "2024-10-19T09:00:00Z",
        "arrival_datetime": "2024-10-19T18:00:00Z"
    }
]
@app.get("/")
def read_root():
    return {"message": "Bienvenidos a la API de viajes"}

@app.get("/flight-events")
def get_flight_events():
    return flight_events
