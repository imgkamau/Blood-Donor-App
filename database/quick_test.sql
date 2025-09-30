-- Quick test queries for the Blood Donor App database
-- Run these in pgAdmin to verify everything works

-- Set the search path
SET search_path TO donate, public;

-- 1. View all donors
SELECT 
    first_name,
    blood_type,
    city,
    is_verified,
    is_available
FROM donate.blood
ORDER BY city, blood_type;

-- 2. Test the search function - Find O+ donors in Nairobi
SELECT * FROM donate.search_donors('O+', -1.286389, 36.817223, 50);

-- 3. Count donors by blood type
SELECT 
    blood_type,
    COUNT(*) as donor_count
FROM donate.blood
WHERE is_available = true
GROUP BY blood_type
ORDER BY donor_count DESC;

-- 4. Test distance calculation
SELECT 
    first_name,
    city,
    ROUND(donate.calculate_distance(-1.286389, 36.817223, latitude, longitude), 2) as distance_from_nairobi_km
FROM donate.blood
WHERE is_available = true
ORDER BY distance_from_nairobi_km;
