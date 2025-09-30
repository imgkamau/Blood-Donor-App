@echo off
echo Setting up Blood Donor App Database...
echo.

REM Check if PostgreSQL is running
echo Checking PostgreSQL connection...
psql -U postgres -h localhost -p 5432 -c "SELECT version();" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Cannot connect to PostgreSQL. Please ensure:
    echo 1. PostgreSQL is running on localhost:5432
    echo 2. User 'postgres' exists with password '123456'
    echo 3. psql is in your PATH
    echo.
    pause
    exit /b 1
)

echo PostgreSQL connection successful!
echo.

REM Create database
echo Creating database 'blood_donor_db'...
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE blood_donor_db;" 2>nul
if %errorlevel% neq 0 (
    echo Database might already exist, continuing...
) else (
    echo Database created successfully!
)
echo.

REM Run setup script
echo Running database setup script...
psql -U postgres -h localhost -p 5432 -d blood_donor_db -f database/setup.sql
if %errorlevel% neq 0 (
    echo ERROR: Failed to run setup script
    pause
    exit /b 1
)

echo.
echo Database setup completed successfully!
echo.
echo You can now run the Flutter app with: flutter run
echo.
pause
