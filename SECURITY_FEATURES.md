# Blood Donor App - Security & Privacy Features

## Implemented Security Measures

### 1. Phone Number Masking
**Purpose:** Protect donor privacy and prevent bulk data harvesting

**Implementation:**
- Phone numbers are masked in search results: `+254719***788`
- Shows first 7 digits and last 3 digits
- Full numbers only stored in database, never exposed via API

**Example:**
- Original: `+254719134788`
- Masked: `+254719***788`

---

### 2. Rate Limiting
**Purpose:** Prevent abuse and automated scraping

**Implementation:**
- Maximum **5 searches per hour** per IP address
- Tracks client IP (supports X-Forwarded-For for proxies)
- Returns HTTP 429 when limit exceeded
- In-memory storage (can be upgraded to Redis for production)

**Response when rate limit exceeded:**
```json
{
  "detail": "Rate limit exceeded. Maximum 5 searches per hour allowed."
}
```

---

### 3. Search Result Limits
**Purpose:** Prevent mass data extraction

**Implementation:**
- **"ANY" blood type searches:** Limited to 5 results
- **Specific blood type searches:** Limited to 10 results
- Results sorted by distance (closest first)

**Rationale:**
- "ANY" searches are more prone to abuse
- Legitimate users searching for specific blood type get more results
- Forces users to be specific about their needs

---

### 4. Minimum Search Radius
**Purpose:** Prevent city-wide or region-wide scraping

**Implementation:**
- Minimum radius: **5 kilometers**
- Returns HTTP 400 if radius < 5km
- Prevents pinpoint location targeting

**Error response:**
```json
{
  "detail": "Minimum search radius is 5km"
}
```

---

### 5. Unique Phone Number Constraint
**Purpose:** Prevent duplicate registrations

**Implementation:**
- Database-level UNIQUE constraint on `phone_number` column
- Uses PostgreSQL's `ON CONFLICT` to update existing records
- Automatically updates donor information if re-registering

**Behavior:**
- First registration: Creates new donor
- Subsequent registrations: Updates existing donor info
- Prevents duplicate phone numbers in system

---

### 6. Optimized Database Indexing
**Purpose:** Improve query performance and reduce server load

**Implemented Indexes:**
1. `idx_blood_blood_type` - Blood type searches
2. `idx_blood_is_available` - Availability filtering
3. `idx_blood_latitude` - Location queries
4. `idx_blood_longitude` - Location queries
5. `idx_blood_city` - City-based searches
6. `idx_blood_search` - Composite index (blood_type + is_available)
7. `idx_blood_location` - Spatial index (lat + long)

**Performance Impact:**
- Faster search queries
- Reduced database load
- Better handling of concurrent requests

---

## Security Configuration

### Rate Limiting Settings
```python
MAX_SEARCHES_PER_HOUR = 5  # Configurable
```

### Result Limits
```python
ANY_BLOOD_TYPE_LIMIT = 5      # For "ANY" searches
SPECIFIC_BLOOD_TYPE_LIMIT = 10 # For specific blood type searches
```

### Minimum Radius
```python
MINIMUM_RADIUS_KM = 5  # Prevents micro-targeted scraping
```

---

## Future Enhancements (Optional)

### 1. Redis for Rate Limiting
- Replace in-memory storage with Redis
- Persist rate limit data across server restarts
- Enable rate limiting across multiple server instances

### 2. Request Logging
- Log all search requests (IP, timestamp, blood_type, location)
- Enable abuse pattern detection
- Analyze usage patterns

### 3. CAPTCHA Integration
- Add CAPTCHA for repeated searches
- Prevent automated bots

### 4. Device Fingerprinting
- Track by device ID in addition to IP
- More accurate rate limiting on mobile apps

### 5. Progressive Restrictions
- First search: 10 results
- Second search: 5 results
- Third+ search: 3 results
- Escalating restrictions for heavy users

---

## Privacy Compliance

✅ **GDPR Compliant**: Phone numbers are masked in responses
✅ **Data Minimization**: Only essential data returned
✅ **Purpose Limitation**: Rate limits prevent bulk extraction
✅ **Access Control**: No authentication required keeps app simple
✅ **Transparency**: Clear error messages inform users of limits

---

## Testing the Security Features

### Test Rate Limiting
```bash
# Make 6 requests rapidly
for i in {1..6}; do
  curl -X POST "https://your-api/api/v1/donors/search" \
    -H "Content-Type: application/json" \
    -d '{"blood_type": "A+", "latitude": -1.286389, "longitude": 36.817223, "radius_km": 10}'
  echo "\n---"
done
# 6th request should return HTTP 429
```

### Test Phone Masking
```bash
# Search and verify phone numbers are masked
curl -X POST "https://your-api/api/v1/donors/search" \
  -H "Content-Type: application/json" \
  -d '{"blood_type": "A+", "latitude": -1.286389, "longitude": 36.817223, "radius_km": 10}'
# Response should show: "+254719***788"
```

### Test Minimum Radius
```bash
# Try with 3km radius (should fail)
curl -X POST "https://your-api/api/v1/donors/search" \
  -H "Content-Type: application/json" \
  -d '{"blood_type": "A+", "latitude": -1.286389, "longitude": 36.817223, "radius_km": 3}'
# Should return HTTP 400
```

---

## Summary

The Blood Donor App now implements multiple layers of security:
- **Privacy Protection**: Phone number masking
- **Abuse Prevention**: Rate limiting + result limits
- **Data Integrity**: Unique phone constraints
- **Performance**: Optimized indexing

All features are **automated** and require **zero manual intervention**.

