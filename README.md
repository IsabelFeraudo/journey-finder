🎯 Journey Finder: RESTful API

This project serves as a backend engineering showcase focused on RESTful API design and service architecture.

It demonstrates:
* RESTful endpoint design following HTTP conventions
* Clean separation of concerns (routing, services, models)
* Business rule implementation and validation logic
* API documentation with OpenAPI / Swagger
* Automated testing with pytest
* Integration between backend services and frontend client
* Mock service architecture for external data sources
* Error handling and response standardization
* The project simulates a real-world backend system that processes domain rules, aggregates data, and exposes structured responses through a public API.

🧰 Tech Stack

* Python 3.10+
* FastAPI
* Uvicorn
* Pytest
* React (frontend demo)
* Node.js

📦 Requirements

* Python 3.10 or higher
* pip
* virtualenv
* Node.js and npm

▶️ Clone and Run the Project
1️⃣ Clone the repository
git clone https://github.com/IsabelFeraudo/journey-finder.git
cd journey-finder
2️⃣ Create a virtual environment

Linux / Mac:

python3 -m venv .venv
source .venv/bin/activate

Windows (PowerShell):

python -m venv .venv
.venv\Scripts\Activate.ps1
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run the APIs
uvicorn backend.main:app --reload --port 8000
uvicorn backend.api.mock_flights_router:app --reload --port 8001

APIs will be available at:
* http://127.0.0.1:8000
* http://127.0.0.1:8001

🔎 Test the API
Search journeys
http://127.0.0.1:8000/journeys/search?date=2024-10-19&from=BUE&to=NYC
Interactive API docs (OpenAPI / Swagger)
http://127.0.0.1:8000/docs
Run automated tests
pytest

This executes all tests in test_journey_service.py.

💻 Frontend Demo (React)
1️⃣ Go to frontend folder
cd frontend
2️⃣ Install dependencies
npm install
3️⃣ Run the app
npm start

Open in browser:

http://localhost:3000
🧭 How to Use the Application

* Enter origin airport code (3 letters)
* Enter destination airport code (3 letters)
* Select departure date
* Click Search journeys
* Results include:
* Connections
* Route (from → to)
* Flight numbers
* Departure and arrival times

📄 Documentation

* Swagger UI: http://127.0.0.1:8000/docs
* OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Test case documentation for mock data:
* documentation/Journey Finder - Test Cases.pdf
