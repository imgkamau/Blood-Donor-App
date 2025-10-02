#!/bin/bash
# Railway startup script for Blood Donor App

echo "🚀 Starting Blood Donor App Backend..."

# Run database setup
echo "📊 Setting up database schema..."
python setup_railway_db.py

# Start the FastAPI server
echo "🌐 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port $PORT

