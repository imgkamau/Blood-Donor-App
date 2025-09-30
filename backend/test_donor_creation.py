#!/usr/bin/env python3
"""
Test donor creation with the exact format the Flutter app sends
"""

import requests
import json

def test_donor_creation():
    print("🧪 Testing Donor Creation...")
    print("-" * 50)
    
    # Test data in the format Flutter app sends
    donor_data = {
        'first_name': 'Test User',
        'phone_number': '+254700000000',
        'blood_type': 'O+',
        'latitude': -1.286389,
        'longitude': 36.817223,
        'address': 'Test Address',
        'city': 'Nairobi',
        'country': 'Kenya',
        'is_verified': False,
        'is_available': True,
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/donors',
            json=donor_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Donor creation: SUCCESS")
        else:
            print(f"❌ Donor creation: FAILED ({response.status_code})")
            
    except Exception as e:
        print(f"❌ Donor creation: ERROR - {e}")

if __name__ == "__main__":
    test_donor_creation()
