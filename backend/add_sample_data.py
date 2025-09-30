#!/usr/bin/env python3
"""
Add sample data to the database for testing
"""

from sqlalchemy import create_engine, text

def add_sample_data():
    print("📊 Adding sample data to database...")
    
    try:
        engine = create_engine("postgresql://postgres:123456@localhost:5432/blood_donor_db")
        
        with engine.connect() as conn:
            # Add sample donors
            sample_donors = [
                {
                    'first_name': 'John',
                    'phone_number': '+254712345678',
                    'blood_type': 'O+',
                    'latitude': -1.286389,
                    'longitude': 36.817223,
                    'address': '123 Nairobi St',
                    'city': 'Nairobi',
                    'country': 'Kenya',
                    'is_verified': True,
                    'is_available': True,
                },
                {
                    'first_name': 'Mary',
                    'phone_number': '+254723456789',
                    'blood_type': 'A+',
                    'latitude': -1.292066,
                    'longitude': 36.821946,
                    'address': '456 Koinange St',
                    'city': 'Nairobi',
                    'country': 'Kenya',
                    'is_verified': True,
                    'is_available': True,
                },
                {
                    'first_name': 'Peter',
                    'phone_number': '+254734567890',
                    'blood_type': 'B+',
                    'latitude': -4.043740,
                    'longitude': 39.668206,
                    'address': '789 Moi Ave',
                    'city': 'Mombasa',
                    'country': 'Kenya',
                    'is_verified': False,
                    'is_available': True,
                },
                {
                    'first_name': 'Sarah',
                    'phone_number': '+254745678901',
                    'blood_type': 'AB+',
                    'latitude': -1.303000,
                    'longitude': 36.780000,
                    'address': '101 Ngong Rd',
                    'city': 'Nairobi',
                    'country': 'Kenya',
                    'is_verified': True,
                    'is_available': True,
                },
                {
                    'first_name': 'David',
                    'phone_number': '+254756789012',
                    'blood_type': 'O-',
                    'latitude': -0.102200,
                    'longitude': 34.767900,
                    'address': '202 Oginga Odinga St',
                    'city': 'Kisumu',
                    'country': 'Kenya',
                    'is_verified': True,
                    'is_available': True,
                }
            ]
            
            for donor in sample_donors:
                conn.execute(text("""
                    INSERT INTO donate.blood (
                        first_name, phone_number, blood_type, latitude, longitude,
                        address, city, country, is_verified, is_available
                    ) VALUES (
                        :first_name, :phone_number, :blood_type, :latitude, :longitude,
                        :address, :city, :country, :is_verified, :is_available
                    )
                """), donor)
            
            conn.commit()
            print(f"✅ Added {len(sample_donors)} sample donors successfully")
            
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")

if __name__ == "__main__":
    add_sample_data()
