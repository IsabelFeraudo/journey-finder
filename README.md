# Journey Finder 🚀

Proyecto de ejemplo de una API para buscar vuelos y viajes combinando uno o más eventos de vuelo. La idea es encontrar rutas desde una ciudad de origen a una ciudad de destino en una fecha determinada, respetando algunas reglas:

- Máximo 2 vuelos por viaje.
- Duración total del viaje ≤ 24 horas.
- Tiempo de conexión ≤ 4 horas.

Se implementa con **Python** y **FastAPI**, y se puede probar desde navegador, Postman o mediante tests automáticos con `pytest`.

---

## Requisitos

- Python 3.10 o superior
- pip
- (Opcional) virtualenv

---

## Clonar y correr el proyecto

### 1️1 Clonar el repositorio

```bash
git clone https://github.com/IsabelFeraudo/journey-finder.git
cd journey-finder

2 Crear un entorno virtual
Linux / Mac:

python3 -m venv .venv
source .venv/bin/activate

Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1

3️ Instalar dependencias
pip install -r requirements.txt

4️ Correr las APIs
journey-finder>
uvicorn backend.main:app --reload --port 8000
uvicorn backend.api.mock_flights_router:app --reload --port 8001


Esto levantará la API en:
http://127.0.0.1:8000

5️ Probar la API
Desde el navegador:

Buscar vuelos:
http://127.0.0.1:8000/journeys/search?date=2024-10-19&from=BUE&to=NYC

Documentación interactiva OpenAPI:http://127.0.0.1:8000/docs

Desde tests automáticos:
pytest
*Esto ejecuta todos los tests de test_journey_service.py.

--

```
