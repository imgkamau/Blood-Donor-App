#!/usr/bin/env python3
"""
Test searching for any blood type vs specific blood type
"""

import requests
import json

def test_any_blood_type_search():
    print("🧪 Testing Any Blood Type Search...")
    print("-" * 50)
    
    # Test 1: Search for ANY blood type
    print("1. Testing 'ANY' blood type search...")
    search_data_any = {
        'blood_type': 'ANY',
        'latitude': -1.286389,
        'longitude': 36.817223,
        'radius_km': 100
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/donors/search',
            json=search_data_any,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Found {len(results)} donors of ANY blood type:")
            for donor in results:
                print(f"   - {donor['first_name']} ({donor['blood_type']}) - {donor['distance_km']:.1f}km away")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 30 + "\n")
    
    # Test 2: Search for specific blood type (O+)
    print("2. Testing specific blood type search (O+)...")
    search_data_specific = {
        'blood_type': 'O+',
        'latitude': -1.286389,
        'longitude': 36.817223,
        'radius_km': 100
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/donors/search',
            json=search_data_specific,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Found {len(results)} donors with O+ blood type:")
            for donor in results:
                print(f"   - {donor['first_name']} ({donor['blood_type']}) - {donor['distance_km']:.1f}km away")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_any_blood_type_search()
