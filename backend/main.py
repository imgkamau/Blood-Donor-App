from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import json
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:YriFkwdSDCFRreklJsMUZnXjJKJVusff@postgres.railway.internal:5432/railway"
)

# Create FastAPI app
app = FastAPI(
    title="Blood Donor App API",
    description="API for Blood Donor App connecting donors and recipients",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.blood_type_subscriptions: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        # Remove from blood type subscriptions
        for blood_type, connections in self.blood_type_subscriptions.items():
            if websocket in connections:
                connections.remove(websocket)

    async def subscribe_to_blood_type(self, websocket: WebSocket, blood_type: str):
        if blood_type not in self.blood_type_subscriptions:
            self.blood_type_subscriptions[blood_type] = []
        if websocket not in self.blood_type_subscriptions[blood_type]:
            self.blood_type_subscriptions[blood_type].append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except:
            self.disconnect(websocket)

    async def broadcast_to_blood_type(self, blood_type: str, message: str):
        if blood_type in self.blood_type_subscriptions:
            for connection in self.blood_type_subscriptions[blood_type].copy():
                try:
                    await connection.send_text(message)
                except:
                    self.disconnect(connection)

    async def broadcast_to_all(self, message: str):
        for connection in self.active_connections.copy():
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

# Initialize database schema
def init_database():
    """Initialize database schema if it doesn't exist"""
    try:
        print("🔍 Checking database connection and schema...")
        with engine.connect() as conn:
            # Check current database
            result = conn.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"✅ Connected to database: {db_name}")
            
            # Create extension first
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            conn.commit()
            print("✅ Extension uuid-ossp created")
            
            # Create table in public schema (for Railway UI visibility)
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS public.blood (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    donor_id UUID,
                    first_name VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL,
                    blood_type VARCHAR(5) NOT NULL CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                    latitude DECIMAL(10, 8) NOT NULL,
                    longitude DECIMAL(11, 8) NOT NULL,
                    address TEXT,
                    city VARCHAR(100),
                    country VARCHAR(100) DEFAULT 'Kenya',
                    is_verified BOOLEAN DEFAULT FALSE,
                    is_available BOOLEAN DEFAULT TRUE,
                    last_donation_date DATE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ Table 'public.blood' created")
            
            # Create indexes
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_blood_type ON public.blood (blood_type)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_latitude ON public.blood (latitude)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_longitude ON public.blood (longitude)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_city ON public.blood (city)"))
            conn.commit()
            print("✅ Indexes created")
            
            # Verify table exists
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'blood'
            """))
            if result.fetchone():
                print("✅ Database schema initialized successfully - Table verified!")
            else:
                print("⚠️  Table was created but not found in schema")
                
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize database schema: {e}")
        print("   The app will still work, but database operations may fail")

# Initialize database on startup
init_database()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class DonorCreate(BaseModel):
    first_name: str
    phone_number: str
    blood_type: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    city: Optional[str] = None
    country: str = "Kenya"
    is_verified: bool = False
    is_available: bool = True

class DonorResponse(BaseModel):
    id: str
    first_name: str
    phone_number: str
    blood_type: str
    latitude: float
    longitude: float
    address: Optional[str]
    city: Optional[str]
    country: str
    is_verified: bool
    is_available: bool
    created_at: str

class DonorSearchRequest(BaseModel):
    blood_type: str
    latitude: float
    longitude: float
    radius_km: float = 50

class DonorSearchResponse(BaseModel):
    id: str
    first_name: str
    phone_number: str
    blood_type: str
    city: Optional[str]
    is_verified: bool
    distance_km: float

# API Routes
@app.get("/")
async def root():
    return {"message": "Blood Donor App API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "healthy", "database": "disconnected", "error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "subscribe_blood_type":
                blood_type = message.get("blood_type")
                if blood_type:
                    await manager.subscribe_to_blood_type(websocket, blood_type)
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "subscribed",
                            "blood_type": blood_type,
                            "message": f"Subscribed to {blood_type} blood requests"
                        }), 
                        websocket
                    )
            
            elif message.get("type") == "ping":
                await manager.send_personal_message(
                    json.dumps({"type": "pong"}), 
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/v1/donors", response_model=DonorResponse)
async def create_donor(donor: DonorCreate, db = Depends(get_db)):
    """Create a new blood donor"""
    try:
        # Insert donor into database
        query = text("""
            INSERT INTO public.blood (
                first_name, phone_number, blood_type, latitude, longitude,
                address, city, country, is_verified, is_available
            ) VALUES (
                :first_name, :phone_number, :blood_type, :latitude, :longitude,
                :address, :city, :country, :is_verified, :is_available
            ) RETURNING id, created_at
        """)
        
        result = db.execute(query, {
            "first_name": donor.first_name,
            "phone_number": donor.phone_number,
            "blood_type": donor.blood_type,
            "latitude": donor.latitude,
            "longitude": donor.longitude,
            "address": donor.address,
            "city": donor.city,
            "country": donor.country,
            "is_verified": donor.is_verified,
            "is_available": donor.is_available
        })
        
        row = result.fetchone()
        donor_id = row[0]
        created_at = row[1]
        
        # Commit the transaction
        db.commit()
        
        # Broadcast new donor to subscribers
        new_donor_message = json.dumps({
            "type": "new_donor",
            "donor": {
                "id": str(donor_id),
                "first_name": donor.first_name,
                "blood_type": donor.blood_type,
                "city": donor.city,
                "is_verified": donor.is_verified,
                "created_at": created_at.isoformat()
            }
        })
        
        # Broadcast to all subscribers of this blood type
        await manager.broadcast_to_blood_type(donor.blood_type, new_donor_message)
        
        return DonorResponse(
            id=str(donor_id),
            first_name=donor.first_name,
            phone_number=donor.phone_number,
            blood_type=donor.blood_type,
            latitude=donor.latitude,
            longitude=donor.longitude,
            address=donor.address,
            city=donor.city,
            country=donor.country,
            is_verified=donor.is_verified,
            is_available=donor.is_available,
            created_at=created_at.isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating donor: {str(e)}")

@app.get("/api/v1/donors", response_model=List[DonorResponse])
async def get_all_donors(db = Depends(get_db)):
    """Get all blood donors"""
    try:
        query = text("""
            SELECT id, first_name, phone_number, blood_type, latitude, longitude,
                   address, city, country, is_verified, is_available, created_at
            FROM public.blood
            WHERE is_available = true
            ORDER BY created_at DESC
        """)
        
        result = db.execute(query)
        donors = []
        
        for row in result:
            donors.append(DonorResponse(
                id=str(row[0]),
                first_name=row[1],
                phone_number=row[2],
                blood_type=row[3],
                latitude=float(row[4]),
                longitude=float(row[5]),
                address=row[6],
                city=row[7],
                country=row[8],
                is_verified=row[9],
                is_available=row[10],
                created_at=row[11].isoformat()
            ))
        
        return donors
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching donors: {str(e)}")

@app.post("/api/v1/donors/search", response_model=List[DonorSearchResponse])
async def search_donors(search_request: DonorSearchRequest, db = Depends(get_db)):
    """Search for donors by blood type and location"""
    try:
        # Haversine formula for distance calculation in PostgreSQL
        distance_formula = """
            6371 * acos(
                cos(radians(:latitude)) * cos(radians(b.latitude)) * 
                cos(radians(b.longitude) - radians(:longitude)) + 
                sin(radians(:latitude)) * sin(radians(b.latitude))
            )
        """
        
        # If blood_type is "ANY", search for all blood types
        if search_request.blood_type.upper() == "ANY":
            query = text(f"""
                SELECT
                    b.id,
                    b.first_name,
                    b.phone_number,
                    b.blood_type,
                    b.city,
                    b.is_verified,
                    {distance_formula} AS distance_km
                FROM
                    public.blood AS b
                WHERE
                    b.is_available = TRUE
                    AND b.is_verified = TRUE
                    AND {distance_formula} <= :radius_km
                ORDER BY
                    distance_km
                LIMIT 20
            """)
            
            result = db.execute(query, {
                "latitude": search_request.latitude,
                "longitude": search_request.longitude,
                "radius_km": search_request.radius_km
            })
        else:
            # Search for specific blood type
            query = text(f"""
                SELECT
                    b.id,
                    b.first_name,
                    b.phone_number,
                    b.blood_type,
                    b.city,
                    b.is_verified,
                    {distance_formula} AS distance_km
                FROM
                    public.blood AS b
                WHERE
                    b.blood_type = :blood_type
                    AND b.is_available = TRUE
                    AND b.is_verified = TRUE
                    AND {distance_formula} <= :radius_km
                ORDER BY
                    distance_km
                LIMIT 20
            """)
            
            result = db.execute(query, {
                "blood_type": search_request.blood_type,
                "latitude": search_request.latitude,
                "longitude": search_request.longitude,
                "radius_km": search_request.radius_km
            })
        
        donors = []
        for row in result:
            # Handle both query formats (ANY search returns 7 columns, specific search returns 14)
            if len(row) == 7:
                # ANY search format
                donors.append(DonorSearchResponse(
                    id=str(row[0]),
                    first_name=row[1],
                    phone_number=row[2],
                    blood_type=row[3],
                    city=row[4],
                    is_verified=row[5],
                    distance_km=float(row[6])
                ))
            else:
                # Specific search format (15 columns)
                donors.append(DonorSearchResponse(
                    id=str(row[0]),
                    first_name=row[1],
                    phone_number=row[2],
                    blood_type=row[3],
                    city=row[7],  # city is at index 7
                    is_verified=row[9],  # is_verified is at index 9
                    distance_km=float(row[14])  # distance_km is at index 14
                ))
        
        return donors
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching donors: {str(e)}")

@app.get("/api/v1/donors/{donor_id}", response_model=DonorResponse)
async def get_donor(donor_id: str, db = Depends(get_db)):
    """Get a specific donor by ID"""
    try:
        query = text("""
            SELECT id, first_name, phone_number, blood_type, latitude, longitude,
                   address, city, country, is_verified, is_available, created_at
            FROM public.blood
            WHERE id = :donor_id
        """)
        
        result = db.execute(query, {"donor_id": donor_id})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Donor not found")
        
        return DonorResponse(
            id=str(row[0]),
            first_name=row[1],
            phone_number=row[2],
            blood_type=row[3],
            latitude=float(row[4]),
            longitude=float(row[5]),
            address=row[6],
            city=row[7],
            country=row[8],
            is_verified=row[9],
            is_available=row[10],
            created_at=row[11].isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching donor: {str(e)}")

@app.put("/api/v1/donors/{donor_id}", response_model=DonorResponse)
async def update_donor(donor_id: str, donor: DonorCreate, db = Depends(get_db)):
    """Update a donor's information"""
    try:
        query = text("""
            UPDATE public.blood SET
                first_name = :first_name,
                phone_number = :phone_number,
                blood_type = :blood_type,
                latitude = :latitude,
                longitude = :longitude,
                address = :address,
                city = :city,
                country = :country,
                is_verified = :is_verified,
                is_available = :is_available,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :donor_id
            RETURNING id, created_at
        """)
        
        result = db.execute(query, {
            "donor_id": donor_id,
            "first_name": donor.first_name,
            "phone_number": donor.phone_number,
            "blood_type": donor.blood_type,
            "latitude": donor.latitude,
            "longitude": donor.longitude,
            "address": donor.address,
            "city": donor.city,
            "country": donor.country,
            "is_verified": donor.is_verified,
            "is_available": donor.is_available
        })
        
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Donor not found")
        
        created_at = row[1]
        
        # Commit the transaction
        db.commit()
        
        return DonorResponse(
            id=donor_id,
            first_name=donor.first_name,
            phone_number=donor.phone_number,
            blood_type=donor.blood_type,
            latitude=donor.latitude,
            longitude=donor.longitude,
            address=donor.address,
            city=donor.city,
            country=donor.country,
            is_verified=donor.is_verified,
            is_available=donor.is_available,
            created_at=created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating donor: {str(e)}")

@app.delete("/api/v1/donors/{donor_id}")
async def delete_donor(donor_id: str, db = Depends(get_db)):
    """Delete a donor"""
    try:
        query = text("DELETE FROM public.blood WHERE id = :donor_id")
        result = db.execute(query, {"donor_id": donor_id})
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Donor not found")
        
        # Commit the transaction
        db.commit()
        
        return {"message": "Donor deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting donor: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
