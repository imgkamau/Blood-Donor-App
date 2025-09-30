# Blood Donor App Backend

FastAPI backend server for the Blood Donor App, connecting the Flutter app to PostgreSQL database.

## Features

- ✅ **FastAPI** with automatic API documentation
- ✅ **PostgreSQL** integration with the `donate.blood` table
- ✅ **CORS** enabled for Flutter app communication
- ✅ **Geospatial search** using custom distance functions
- ✅ **RESTful API** endpoints for donor management

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python run_server.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/donors` | Create new donor |
| GET | `/donors` | Get all donors |
| GET | `/donors/{id}` | Get specific donor |
| PUT | `/donors/{id}` | Update donor |
| DELETE | `/donors/{id}` | Delete donor |
| POST | `/donors/search` | Search donors by location |

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Connection

The backend connects to:
- **Host**: localhost:5432
- **Database**: blood_donor_db
- **Schema**: donate
- **Table**: blood

## Example API Calls

### Create a Donor
```bash
curl -X POST "http://localhost:8000/api/v1/donors" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "phone_number": "+254712345678",
    "blood_type": "O+",
    "latitude": -1.286389,
    "longitude": 36.817223,
    "city": "Nairobi"
  }'
```

### Search Donors
```bash
curl -X POST "http://localhost:8000/api/v1/donors/search" \
  -H "Content-Type: application/json" \
  -d '{
    "blood_type": "O+",
    "latitude": -1.286389,
    "longitude": 36.817223,
    "radius_km": 50
  }'
```

## Development

The server runs with auto-reload enabled, so changes to the code will automatically restart the server.

## Testing

Test the API endpoints using the interactive documentation at http://localhost:8000/docs
