-- Blood Donor App Database Setup
-- PostgreSQL with PostGIS extension

-- Create database (run this separately)
-- CREATE DATABASE blood_donor_db;

-- Connect to the database and create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create donors table
CREATE TABLE IF NOT EXISTS donors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
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

-- Create recipients table
CREATE TABLE IF NOT EXISTS recipients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    blood_type VARCHAR(5) NOT NULL CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    location GEOMETRY(POINT, 4326),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Kenya',
    search_count INTEGER DEFAULT 0,
    last_search TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create payments table
CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipient_id UUID REFERENCES recipients(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'KES',
    payment_method VARCHAR(20) NOT NULL CHECK (payment_method IN ('mpesa', 'card', 'bank')),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'cancelled')),
    mpesa_receipt_number VARCHAR(50),
    transaction_id VARCHAR(100),
    phone_number VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create search_history table
CREATE TABLE IF NOT EXISTS search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipient_id UUID REFERENCES recipients(id) ON DELETE CASCADE,
    blood_type VARCHAR(5) NOT NULL,
    search_radius DECIMAL(8,2) NOT NULL,
    user_location GEOMETRY(POINT, 4326) NOT NULL,
    donor_count INTEGER DEFAULT 0,
    payment_id UUID REFERENCES payments(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_donors_blood_type ON donors(blood_type);
CREATE INDEX IF NOT EXISTS idx_donors_location ON donors USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_donors_available ON donors(is_available);
CREATE INDEX IF NOT EXISTS idx_recipients_location ON recipients USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_payments_recipient ON payments(recipient_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_search_history_recipient ON search_history(recipient_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(is_read);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_donors_updated_at BEFORE UPDATE ON donors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recipients_updated_at BEFORE UPDATE ON recipients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing
INSERT INTO users (id, email, phone_number, first_name, is_verified) VALUES
    ('550e8400-e29b-41d4-a716-446655440001', 'john@example.com', '+254712345678', 'John', true),
    ('550e8400-e29b-41d4-a716-446655440002', 'mary@example.com', '+254723456789', 'Mary', true),
    ('550e8400-e29b-41d4-a716-446655440003', 'peter@example.com', '+254734567890', 'Peter', false)
ON CONFLICT (id) DO NOTHING;

INSERT INTO donors (id, user_id, first_name, phone_number, blood_type, location, city, is_verified, is_available) VALUES
    ('650e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'John', '+254712345678', 'O+', ST_SetSRID(ST_MakePoint(36.817223, -1.286389), 4326), 'Nairobi', true, true),
    ('650e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440002', 'Mary', '+254723456789', 'A+', ST_SetSRID(ST_MakePoint(36.817223, -1.286389), 4326), 'Nairobi', true, true),
    ('650e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440003', 'Peter', '+254734567890', 'B+', ST_SetSRID(ST_MakePoint(39.668206, -4.043740), 4326), 'Mombasa', false, true)
ON CONFLICT (id) DO NOTHING;

-- Create view for donor search with distance calculation
CREATE OR REPLACE VIEW donor_search_view AS
SELECT 
    d.id,
    d.first_name,
    d.phone_number,
    d.blood_type,
    d.city,
    d.is_verified,
    d.is_available,
    ST_X(d.location) as latitude,
    ST_Y(d.location) as longitude,
    d.created_at
FROM donors d
WHERE d.is_available = true;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON DATABASE blood_donor_db TO postgres;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
