#!/usr/bin/env python3
"""
Test script for Railway deployed backend
"""
import requests
import json

# Replace with your actual Railway URL
RAILWAY_URL = "https://blood-donor-app-production-aa1d.up.railway.app"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Railway backend health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Railway backend: {e}")
        return False

def test_donor_search():
    """Test donor search"""
    try:
        search_data = {
            "blood_type": "O+",
            "latitude": -1.286389,
            "longitude": 36.817223,
            "radius_km": 50
        }
        
        response = requests.post(
            f"{RAILWAY_URL}/api/v1/donors/search",
            json=search_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Railway backend donor search working")
            return True
        else:
            print(f"❌ Donor search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Donor search error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Railway Backend")
    print("=" * 30)
    print(f"Testing URL: {RAILWAY_URL}")
    print()
    
    if test_health():
        test_donor_search()
    
    print("\n🎉 Railway backend test completed!")
