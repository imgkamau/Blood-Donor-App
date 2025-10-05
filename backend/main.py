from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import json
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Rate limiting storage (in-memory for simplicity)
# In production, use Redis or a database
search_rate_limit = defaultdict(list)
MAX_SEARCHES_PER_HOUR = 5

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
                    phone_number VARCHAR(20) NOT NULL UNIQUE,
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
            
            # Add unique constraint to phone_number if table already exists
            conn.execute(text("""
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'blood_phone_number_key'
                    ) THEN
                        ALTER TABLE public.blood ADD CONSTRAINT blood_phone_number_key UNIQUE (phone_number);
                    END IF;
                END $$;
            """))
            conn.commit()
            print("✅ Unique constraint on phone_number ensured")
            
            # Create indexes for better query performance
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_blood_type ON public.blood (blood_type)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_is_available ON public.blood (is_available)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_latitude ON public.blood (latitude)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_longitude ON public.blood (longitude)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_city ON public.blood (city)"))
            
            # Composite index for common search queries (blood_type + is_available)
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_search ON public.blood (blood_type, is_available) WHERE is_available = TRUE"))
            
            # Spatial index for efficient location-based queries
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_blood_location ON public.blood (latitude, longitude)"))
            
            conn.commit()
            print("✅ Indexes created")
            
            # Create search_logs table for admin portal
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS public.search_logs (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    blood_type VARCHAR(5) NOT NULL,
                    latitude DECIMAL(10, 8) NOT NULL,
                    longitude DECIMAL(11, 8) NOT NULL,
                    radius_km DECIMAL(8, 2) NOT NULL,
                    results_count INTEGER NOT NULL DEFAULT 0,
                    client_ip VARCHAR(45),
                    searched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ Table 'public.search_logs' created")
            
            # Create index on search_logs
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_search_logs_searched_at ON public.search_logs (searched_at DESC)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_search_logs_blood_type ON public.search_logs (blood_type)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_search_logs_client_ip ON public.search_logs (client_ip)"))
            conn.commit()
            print("✅ Search logs indexes created")
            
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

# Utility Functions
def mask_phone_number(phone: str) -> str:
    """Mask phone number for privacy: +254719***788"""
    if not phone or len(phone) < 8:
        return phone
    # Show first 7 characters and last 3
    return f"{phone[:7]}***{phone[-3:]}"

def check_rate_limit(client_id: str) -> bool:
    """Check if client has exceeded rate limit"""
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    
    # Remove old entries
    search_rate_limit[client_id] = [
        timestamp for timestamp in search_rate_limit[client_id]
        if timestamp > one_hour_ago
    ]
    
    # Check if limit exceeded
    if len(search_rate_limit[client_id]) >= MAX_SEARCHES_PER_HOUR:
        return False
    
    # Add new search timestamp
    search_rate_limit[client_id].append(now)
    return True

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
    """Create a new blood donor or update existing one if phone number already exists"""
    try:
        # First check if phone number exists
        check_query = text("""
            SELECT id, created_at FROM public.blood WHERE phone_number = :phone_number
        """)
        existing = db.execute(check_query, {"phone_number": donor.phone_number}).fetchone()
        
        if existing:
            # Update existing donor
            update_query = text("""
                UPDATE public.blood SET
                    first_name = :first_name,
                    blood_type = :blood_type,
                    latitude = :latitude,
                    longitude = :longitude,
                    address = :address,
                    city = :city,
                    country = :country,
                    is_available = :is_available,
                    updated_at = CURRENT_TIMESTAMP
                WHERE phone_number = :phone_number
                RETURNING id, created_at
            """)
            result = db.execute(update_query, {
                "first_name": donor.first_name,
                "phone_number": donor.phone_number,
                "blood_type": donor.blood_type,
                "latitude": donor.latitude,
                "longitude": donor.longitude,
                "address": donor.address,
                "city": donor.city,
                "country": donor.country,
                "is_available": donor.is_available
            })
        else:
            # Insert new donor
            insert_query = text("""
                INSERT INTO public.blood (
                    first_name, phone_number, blood_type, latitude, longitude,
                    address, city, country, is_verified, is_available
                ) VALUES (
                    :first_name, :phone_number, :blood_type, :latitude, :longitude,
                    :address, :city, :country, :is_verified, :is_available
                ) RETURNING id, created_at
            """)
            result = db.execute(insert_query, {
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
async def search_donors(search_request: DonorSearchRequest, request: Request, db = Depends(get_db)):
    """Search for donors by blood type and location with rate limiting and privacy protection"""
    try:
        # Get client identifier (IP address or X-Forwarded-For header)
        client_ip = request.client.host if request.client else "unknown"
        forwarded_for = request.headers.get("X-Forwarded-For")
        client_id = forwarded_for.split(",")[0] if forwarded_for else client_ip
        
        # Check rate limit
        if not check_rate_limit(client_id):
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded. Maximum {MAX_SEARCHES_PER_HOUR} searches per hour allowed."
            )
        
        # Validate minimum search radius (prevent city-wide scraping)
        if search_request.radius_km < 5:
            raise HTTPException(
                status_code=400,
                detail="Minimum search radius is 5km"
            )
        
        # Haversine formula for distance calculation in PostgreSQL
        distance_formula = """
            6371 * acos(
                cos(radians(:latitude)) * cos(radians(b.latitude)) * 
                cos(radians(b.longitude) - radians(:longitude)) + 
                sin(radians(:latitude)) * sin(radians(b.latitude))
            )
        """
        
        # If blood_type is "ANY", limit results more strictly
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
                    AND {distance_formula} <= :radius_km
                ORDER BY
                    distance_km
                LIMIT 5
            """)
            
            result = db.execute(query, {
                "latitude": search_request.latitude,
                "longitude": search_request.longitude,
                "radius_km": search_request.radius_km
            })
        else:
            # Search for specific blood type (allow more results)
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
                    AND {distance_formula} <= :radius_km
                ORDER BY
                    distance_km
                LIMIT 10
            """)
            
            result = db.execute(query, {
                "blood_type": search_request.blood_type,
                "latitude": search_request.latitude,
                "longitude": search_request.longitude,
                "radius_km": search_request.radius_km
            })
        
        donors = []
        for row in result:
            # Mask phone number for privacy
            masked_phone = mask_phone_number(row[2])
            
            # All queries now return 7 columns
            donors.append(DonorSearchResponse(
                id=str(row[0]),
                first_name=row[1],
                phone_number=masked_phone,
                blood_type=row[3],
                city=row[4],
                is_verified=row[5],
                distance_km=float(row[6])
            ))
        
        # Log the search activity (async, don't block response)
        try:
            log_query = text("""
                INSERT INTO public.search_logs (
                    blood_type, latitude, longitude, radius_km, results_count, client_ip
                ) VALUES (
                    :blood_type, :latitude, :longitude, :radius_km, :results_count, :client_ip
                )
            """)
            db.execute(log_query, {
                "blood_type": search_request.blood_type,
                "latitude": search_request.latitude,
                "longitude": search_request.longitude,
                "radius_km": search_request.radius_km,
                "results_count": len(donors),
                "client_ip": client_id
            })
            db.commit()
        except Exception as log_error:
            # Don't fail the request if logging fails
            print(f"Warning: Failed to log search activity: {log_error}")
        
        return donors
        
    except HTTPException:
        raise
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

# ============================================
# ADMIN PORTAL ENDPOINTS
# ============================================

@app.get("/api/v1/admin/stats")
async def get_admin_stats(db = Depends(get_db)):
    """Get statistics for admin dashboard"""
    try:
        print("📊 Fetching admin stats...")
        
        # Total donors
        total_donors_result = db.execute(text("SELECT COUNT(*) as count FROM public.blood")).fetchone()
        total_donors = total_donors_result[0]
        print(f"✅ Total donors: {total_donors}")
        
        # Donors by blood type
        donors_by_blood_type = db.execute(text("""
            SELECT blood_type, COUNT(*) as count 
            FROM public.blood 
            GROUP BY blood_type 
            ORDER BY blood_type
        """)).fetchall()
        print(f"✅ Donors by blood type: {len(donors_by_blood_type)} types")
        
        # Recent donors (last 5)
        recent_donors = db.execute(text("""
            SELECT id, first_name, blood_type, city, latitude, longitude, created_at
            FROM public.blood 
            ORDER BY created_at DESC 
            LIMIT 5
        """)).fetchall()
        print(f"✅ Recent donors: {len(recent_donors)} donors")
        
        # Total searches - handle table not existing
        try:
            search_count_result = db.execute(text("SELECT COUNT(*) as count FROM public.search_logs")).fetchone()
            search_count = search_count_result[0] if search_count_result else 0
            print(f"✅ Search count: {search_count}")
        except Exception as search_error:
            print(f"⚠️ Search logs table doesn't exist yet: {search_error}")
            # Rollback the failed transaction to continue
            db.rollback()
            search_count = 0
        
        # Today's registrations
        today_registrations_result = db.execute(text("""
            SELECT COUNT(*) as count 
            FROM public.blood 
            WHERE created_at >= CURRENT_DATE
        """)).fetchone()
        today_registrations = today_registrations_result[0]
        print(f"✅ Today's registrations: {today_registrations}")
        
        # Top cities
        top_cities = db.execute(text("""
            SELECT city, COUNT(*) as count 
            FROM public.blood 
            WHERE city IS NOT NULL
            GROUP BY city 
            ORDER BY count DESC 
            LIMIT 5
        """)).fetchall()
        print(f"✅ Top cities: {len(top_cities)} cities")
        
        result = {
            "totalDonors": total_donors,
            "donorsByBloodType": [{"blood_type": row[0], "count": row[1]} for row in donors_by_blood_type],
            "recentDonors": [
                {
                    "id": str(row[0]),
                    "first_name": row[1],
                    "blood_type": row[2],
                    "location": row[3] or f"{row[4]}, {row[5]}",
                    "created_at": row[6].isoformat()
                } for row in recent_donors
            ],
            "searchCount": search_count,
            "todayRegistrations": today_registrations,
            "topCities": [{"city": row[0], "count": row[1]} for row in top_cities]
        }
        
        print("✅ Admin stats fetched successfully")
        return result
        
    except Exception as e:
        print(f"❌ Error fetching admin stats: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching admin stats: {str(e)}")


@app.get("/api/v1/admin/donors")
async def get_all_donors(
    search: Optional[str] = None,
    blood_type: Optional[str] = None,
    db = Depends(get_db)
):
    """Get all donors with optional filters"""
    try:
        query_text = """
            SELECT id, first_name, phone_number, blood_type, city, latitude, longitude,
                   is_verified, is_available, created_at 
            FROM public.blood 
            WHERE 1=1
        """
        params = {}
        
        if search:
            query_text += """ AND (
                first_name ILIKE :search 
                OR phone_number ILIKE :search 
                OR city ILIKE :search
            )"""
            params["search"] = f"%{search}%"
        
        if blood_type and blood_type != "all":
            query_text += " AND blood_type = :blood_type"
            params["blood_type"] = blood_type
        
        query_text += " ORDER BY created_at DESC"
        
        results = db.execute(text(query_text), params).fetchall()
        
        return [
            {
                "id": str(row[0]),
                "first_name": row[1],
                "phone": row[2],
                "blood_type": row[3],
                "location": row[4] or f"{row[5]}, {row[6]}",
                "is_verified": row[7],
                "is_available": row[8],
                "created_at": row[9].isoformat()
            } for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching donors: {str(e)}")


@app.get("/api/v1/admin/search-activity")
async def get_search_activity(
    blood_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    db = Depends(get_db)
):
    """Get search activity logs"""
    try:
        query_text = """
            SELECT id, blood_type, latitude, longitude, radius_km,
                   results_count, client_ip, searched_at 
            FROM public.search_logs 
            WHERE 1=1
        """
        params = {}
        
        if blood_type and blood_type != "all":
            query_text += " AND blood_type = :blood_type"
            params["blood_type"] = blood_type
        
        if date_from:
            query_text += " AND searched_at >= :date_from"
            params["date_from"] = date_from
        
        if date_to:
            query_text += " AND searched_at <= :date_to"
            params["date_to"] = date_to
        
        query_text += " ORDER BY searched_at DESC LIMIT 100"
        
        results = db.execute(text(query_text), params).fetchall()
        
        return [
            {
                "id": str(row[0]),
                "blood_type": row[1],
                "latitude": float(row[2]),
                "longitude": float(row[3]),
                "radius_km": float(row[4]),
                "results_count": row[5],
                "client_ip": row[6],
                "searched_at": row[7].isoformat()
            } for row in results
        ]
    except Exception as e:
        # If table doesn't exist yet, return empty array
        return []


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
