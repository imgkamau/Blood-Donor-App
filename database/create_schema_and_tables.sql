-- Blood Donor App Database Schema Creation
-- Run this script in pgAdmin to create the schema and tables

-- Create the 'donate' schema
CREATE SCHEMA IF NOT EXISTS donate;

-- Set the search path to include the donate schema
SET search_path TO donate, public;

-- Create extensions in the donate schema
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" SCHEMA donate;
CREATE EXTENSION IF NOT EXISTS "postgis" SCHEMA donate;

-- Create the blood table in the donate schema
CREATE TABLE IF NOT EXISTS donate.blood (
    id UUID PRIMARY KEY DEFAULT donate.uuid_generate_v4(),
    donor_id UUID,
    first_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    blood_type VARCHAR(5) NOT NULL CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    location GEOMETRY(POINT, 4326) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Kenya',
    is_verified BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    last_donation_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_blood_blood_type ON donate.blood(blood_type);
CREATE INDEX IF NOT EXISTS idx_blood_location ON donate.blood USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_blood_available ON donate.blood(is_available);
CREATE INDEX IF NOT EXISTS idx_blood_city ON donate.blood(city);
CREATE INDEX IF NOT EXISTS idx_blood_created_at ON donate.blood(created_at);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION donate.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_blood_updated_at 
    BEFORE UPDATE ON donate.blood
    FOR EACH ROW 
    EXECUTE FUNCTION donate.update_updated_at_column();

-- Insert sample data for testing
INSERT INTO donate.blood (id, first_name, phone_number, blood_type, location, city, is_verified, is_available) VALUES
    ('550e8400-e29b-41d4-a716-446655440001', 'John', '+254712345678', 'O+', ST_SetSRID(ST_MakePoint(36.817223, -1.286389), 4326), 'Nairobi', true, true),
    ('550e8400-e29b-41d4-a716-446655440002', 'Mary', '+254723456789', 'A+', ST_SetSRID(ST_MakePoint(36.817223, -1.286389), 4326), 'Nairobi', true, true),
    ('550e8400-e29b-41d4-a716-446655440003', 'Peter', '+254734567890', 'B+', ST_SetSRID(ST_MakePoint(39.668206, -4.043740), 4326), 'Mombasa', false, true),
    ('550e8400-e29b-41d4-a716-446655440004', 'Sarah', '+254745678901', 'AB+', ST_SetSRID(ST_MakePoint(36.817223, -1.286389), 4326), 'Nairobi', true, true),
    ('550e8400-e29b-41d4-a716-446655440005', 'David', '+254756789012', 'O-', ST_SetSRID(ST_MakePoint(35.302722, -0.023559), 4326), 'Kisumu', true, true),
    ('550e8400-e29b-41d4-a716-446655440006', 'Grace', '+254767890123', 'A-', ST_SetSRID(ST_MakePoint(36.817223, -1.286389), 4326), 'Nairobi', false, true),
    ('550e8400-e29b-41d4-a716-446655440007', 'James', '+254778901234', 'B-', ST_SetSRID(ST_MakePoint(39.668206, -4.043740), 4326), 'Mombasa', true, true),
    ('550e8400-e29b-41d4-a716-446655440008', 'Linda', '+254789012345', 'AB-', ST_SetSRID(ST_MakePoint(36.817223, -1.286389), 4326), 'Nairobi', true, true)
ON CONFLICT (id) DO NOTHING;

-- Create a view for easy querying with distance calculations
CREATE OR REPLACE VIEW donate.blood_donors_view AS
SELECT 
    id,
    first_name,
    phone_number,
    blood_type,
    city,
    is_verified,
    is_available,
    ST_X(location) as latitude,
    ST_Y(location) as longitude,
    created_at,
    updated_at
FROM donate.blood
WHERE is_available = true;

-- Create a function to search donors by blood type and location
CREATE OR REPLACE FUNCTION donate.search_donors(
    p_blood_type VARCHAR(5),
    p_latitude DECIMAL,
    p_longitude DECIMAL,
    p_radius_km DECIMAL DEFAULT 50
)
RETURNS TABLE (
    id UUID,
    first_name VARCHAR(100),
    phone_number VARCHAR(20),
    blood_type VARCHAR(5),
    city VARCHAR(100),
    is_verified BOOLEAN,
    distance_km DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        b.id,
        b.first_name,
        b.phone_number,
        b.blood_type,
        b.city,
        b.is_verified,
        ROUND(
            ST_Distance(
                b.location,
                ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)::geography
            ) / 1000.0, 2
        ) as distance_km
    FROM donate.blood b
    WHERE b.blood_type = p_blood_type
        AND b.is_available = true
        AND ST_DWithin(
            b.location,
            ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)::geography,
            p_radius_km * 1000
        )
    ORDER BY distance_km ASC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON SCHEMA donate TO postgres;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA donate TO postgres;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA donate TO postgres;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA donate TO postgres;

-- Display success message
DO $$
BEGIN
    RAISE NOTICE 'Blood Donor App database schema created successfully!';
    RAISE NOTICE 'Schema: donate';
    RAISE NOTICE 'Table: blood';
    RAISE NOTICE 'Sample data: 8 donors inserted';
    RAISE NOTICE 'View: blood_donors_view';
    RAISE NOTICE 'Function: search_donors()';
END $$;
