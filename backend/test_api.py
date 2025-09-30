#!/usr/bin/env python3
"""
Test script to verify the Blood Donor App API is working
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Blood Donor App API...")
    print("-" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")
    
    # Test 2: Get all donors
    try:
        response = requests.get(f"{base_url}/api/v1/donors")
        if response.status_code == 200:
            donors = response.json()
            print(f"✅ Get donors: PASSED ({len(donors)} donors found)")
            if donors:
                print(f"   Sample donor: {donors[0]['first_name']} ({donors[0]['blood_type']})")
        else:
            print(f"❌ Get donors: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Get donors: ERROR - {e}")
    
    # Test 3: Search donors
    try:
        search_data = {
            "blood_type": "O+",
            "latitude": -1.286389,
            "longitude": 36.817223,
            "radius_km": 50
        }
        response = requests.post(
            f"{base_url}/api/v1/donors/search",
            json=search_data
        )
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Search donors: PASSED ({len(results)} results)")
            if results:
                print(f"   Nearest donor: {results[0]['first_name']} ({results[0]['distance_km']}km away)")
        else:
            print(f"❌ Search donors: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Search donors: ERROR - {e}")
    
    print("-" * 50)
    print("🎉 API testing completed!")
    print(f"📊 API Documentation: {base_url}/docs")

if __name__ == "__main__":
    test_api()
