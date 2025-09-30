#!/bin/bash

echo "Setting up Blood Donor App Database..."
echo

# Check if PostgreSQL is running
echo "Checking PostgreSQL connection..."
psql -U postgres -h localhost -p 5432 -c "SELECT version();" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Cannot connect to PostgreSQL. Please ensure:"
    echo "1. PostgreSQL is running on localhost:5432"
    echo "2. User 'postgres' exists with password '123456'"
    echo "3. psql is in your PATH"
    echo
    exit 1
fi

echo "PostgreSQL connection successful!"
echo

# Create database
echo "Creating database 'blood_donor_db'..."
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE blood_donor_db;" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Database might already exist, continuing..."
else
    echo "Database created successfully!"
fi
echo

# Run setup script
echo "Running database setup script..."
psql -U postgres -h localhost -p 5432 -d blood_donor_db -f database/setup.sql
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run setup script"
    exit 1
fi

echo
echo "Database setup completed successfully!"
echo
echo "You can now run the Flutter app with: flutter run"
echo
