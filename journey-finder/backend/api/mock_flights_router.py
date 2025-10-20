from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mock Flight Events API")

# Permitir CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos de ejemplo
flight_events = [
    {"flight_number": "IB1234", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2024-10-19T08:00:00Z", "arrival_datetime": "2024-10-19T14:00:00Z"},
    {"flight_number": "IB2345", "departure_city": "BUE", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T16:00:00Z", "arrival_datetime": "2024-10-19T22:00:00Z"},
    {"flight_number": "IB3456", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T09:00:00Z", "arrival_datetime": "2024-10-19T18:00:00Z"}
]

@app.get("/flight-events")
def get_flight_events():
    """Devuelve todos los vuelos mock"""
    return flight_events
