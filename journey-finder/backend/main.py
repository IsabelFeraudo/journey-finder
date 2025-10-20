from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.journeys_router import router as journeys_router

app = FastAPI(title="Flight Events API")

app.include_router(journeys_router, prefix="/journeys")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenidos a la API de viajes"}
