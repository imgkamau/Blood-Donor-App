#!/usr/bin/env python3
"""
Blood Donor App Backend Server
Run this script to start the FastAPI server
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting Blood Donor App Backend Server...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000/api/v1")
    print("💾 Database: PostgreSQL (blood_donor_db)")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",  # Use import string for reload to work
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
