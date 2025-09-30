-- Test queries for the Blood Donor App database
-- Run these queries in pgAdmin to test the database setup

-- Set the search path to include the donate schema
SET search_path TO donate, public;

-- 1. View all donors
SELECT 
    first_name,
    blood_type,
    city,
    is_verified,
    is_available,
    created_at
FROM donate.blood
ORDER BY created_at DESC;

-- 2. Count donors by blood type
SELECT 
    blood_type,
    COUNT(*) as donor_count
FROM donate.blood
WHERE is_available = true
GROUP BY blood_type
ORDER BY donor_count DESC;

-- 3. Count donors by city
SELECT 
    city,
    COUNT(*) as donor_count
FROM donate.blood
WHERE is_available = true
GROUP BY city
ORDER BY donor_count DESC;

-- 4. Search for O+ donors in Nairobi (within 50km)
SELECT * FROM donate.search_donors('O+', -1.286389, 36.817223, 50);

-- 5. Search for A+ donors in Mombasa (within 30km)
SELECT * FROM donate.search_donors('A+', -4.043740, 39.668206, 30);

-- 6. Find all verified donors
SELECT 
    first_name,
    blood_type,
    city,
    phone_number
FROM donate.blood
WHERE is_verified = true AND is_available = true
ORDER BY city, blood_type;

-- 7. Test the view
SELECT * FROM donate.blood_donors_view
WHERE blood_type = 'O+'
ORDER BY created_at DESC;

-- 8. Find donors within 100km of a specific location (Kisumu)
SELECT 
    first_name,
    blood_type,
    city,
    ROUND(
        ST_Distance(
            location,
            ST_SetSRID(ST_MakePoint(35.302722, -0.023559), 4326)::geography
        ) / 1000.0, 2
    ) as distance_km
FROM donate.blood
WHERE is_available = true
    AND ST_DWithin(
        location,
        ST_SetSRID(ST_MakePoint(35.302722, -0.023559), 4326)::geography,
        100000
    )
ORDER BY distance_km ASC;

-- 9. Insert a new test donor
INSERT INTO donate.blood (first_name, phone_number, blood_type, location, city, is_verified, is_available)
VALUES (
    'Test Donor',
    '+254799999999',
    'O+',
    ST_SetSRID(ST_MakePoint(36.817223, -1.286389), 4326),
    'Nairobi',
    true,
    true
);

-- 10. Update a donor's availability
UPDATE donate.blood 
SET is_available = false, updated_at = CURRENT_TIMESTAMP
WHERE first_name = 'Test Donor';

-- 11. Delete the test donor
DELETE FROM donate.blood WHERE first_name = 'Test Donor';

-- 12. Show database statistics
SELECT 
    'Total Donors' as metric,
    COUNT(*) as value
FROM donate.blood
UNION ALL
SELECT 
    'Available Donors',
    COUNT(*)
FROM donate.blood
WHERE is_available = true
UNION ALL
SELECT 
    'Verified Donors',
    COUNT(*)
FROM donate.blood
WHERE is_verified = true
UNION ALL
SELECT 
    'Unique Blood Types',
    COUNT(DISTINCT blood_type)
FROM donate.blood
UNION ALL
SELECT 
    'Cities Covered',
    COUNT(DISTINCT city)
FROM donate.blood;
