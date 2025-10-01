#!/usr/bin/env python3
"""
Test script to verify RDS connection and API endpoints
"""
import requests
import json
import sys

# RDS Backend URL (you'll need to deploy this or use a tunnel)
BACKEND_URL = "http://localhost:8000"  # Change this to your deployed backend URL

def test_health_endpoint():
    """Test if the backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_donor_creation():
    """Test donor creation endpoint"""
    try:
        donor_data = {
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+254700000000",
            "blood_type": "O+",
            "city": "Nairobi",
            "latitude": -1.286389,
            "longitude": 36.817223,
            "is_verified": False
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/v1/donors",
            json=donor_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Donor creation working")
            donor_id = response.json().get("id")
            print(f"   Created donor ID: {donor_id}")
            return True
        else:
            print(f"❌ Donor creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Donor creation request failed: {e}")
        return False

def test_donor_search():
    """Test donor search endpoint"""
    try:
        search_data = {
            "blood_type": "O+",
            "latitude": -1.286389,
            "longitude": 36.817223,
            "radius_km": 50
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/v1/donors/search",
            json=search_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Donor search working")
            results = response.json()
            if isinstance(results, list):
                print(f"   Found {len(results)} donors")
            else:
                print(f"   Found {len(results.get('donors', []))} donors")
            return True
        else:
            print(f"❌ Donor search failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Donor search request failed: {e}")
        return False

def main():
    print("🧪 Testing RDS Backend Connection")
    print("=" * 40)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("\n❌ Backend is not running or not accessible")
        print("Please start your backend server with: python backend/run_server.py")
        sys.exit(1)
    
    # Test donor creation
    test_donor_creation()
    
    # Test donor search
    test_donor_search()
    
    print("\n" + "=" * 40)
    print("🎉 Backend tests completed!")

if __name__ == "__main__":
    main()
