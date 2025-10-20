from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mock Flight Events API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos de ejemplo para probar la logica de la API. *Ver test_journey_service.py
flight_events = [
    {"flight_number": "IB1234", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2024-10-19T08:00:00Z", "arrival_datetime": "2024-10-19T14:00:00Z"},
    {"flight_number": "IB2345", "departure_city": "BUE", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T16:00:00Z", "arrival_datetime": "2024-10-19T22:00:00Z"},
    {"flight_number": "IB3456", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T09:00:00Z", "arrival_datetime": "2024-10-19T18:00:00Z"},
    {"flight_number": "IB4567", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-19T11:00:00Z"},
    {"flight_number": "IB5678", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T12:30:00Z", "arrival_datetime": "2024-10-19T18:30:00Z"},
    {"flight_number": "IB6789", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-19T11:00:00Z"},
    {"flight_number": "IB7890", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-19T16:30:00Z", "arrival_datetime": "2024-10-19T22:30:00Z"},
    {"flight_number": "IB8901", "departure_city": "BUE", "arrival_city": "MAD",
     "departure_datetime": "2024-10-19T05:00:00Z", "arrival_datetime": "2024-10-20T06:00:00Z"},
    {"flight_number": "IB9012", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-20T06:30:00Z", "arrival_datetime": "2024-10-20T12:30:00Z"},

    {"flight_number": "VD1001", "departure_city": "MAD", "arrival_city": "NYC",
     "departure_datetime": "2024-10-20T23:00:00Z", "arrival_datetime": "2024-10-21T01:00:00Z"},
    

    {"flight_number": "VC2001", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2024-10-20T21:00:00Z", "arrival_datetime": "2024-10-20T22:00:00Z"},
    {"flight_number": "VC2002", "departure_city": "BUE", "arrival_city": "NYC",
     "departure_datetime": "2024-10-20T23:00:00Z", "arrival_datetime": "2024-10-21T01:00:00Z"},
    

    {"flight_number": "VC3001", "departure_city": "MAD", "arrival_city": "BUE",
     "departure_datetime": "2024-10-20T22:00:00Z", "arrival_datetime": "2024-10-20T23:00:00Z"},
    {"flight_number": "VC3002", "departure_city": "BUE", "arrival_city": "NYC",
     "departure_datetime": "2024-10-21T01:00:00Z", "arrival_datetime": "2024-10-21T02:00:00Z"},
]



@app.get("/flight-events")
def get_flight_events():
    """Devuelve todos los vuelos mock"""
    return flight_events
