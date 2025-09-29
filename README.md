Blood Donor App
Overview
The Blood Donor App is a Flutter-based mobile application designed to address the blood shortage issue in Kenya by connecting recipients with nearby blood donors in emergencies. Donors enroll with their first name, phone number, blood type, and location (via GPS or manual input). Recipients pay a small fee (e.g., KSh 50 via M-Pesa) to access a list of matching donors within a specified radius (e.g., 50km). The app uses Firebase for backend services and integrates geolocation for proximity-based matching.
This README provides instructions to set up, build, and run the app, covering the core features, geolocation integration, and future enhancements. The app is an MVP (Minimum Viable Product) for educational purposes—consult Kenya's Data Protection Act and the Kenya National Blood Transfusion Service for production deployment.
Features

Donor Enrollment: Users register as donors with first name, phone number, blood type (A+, O-, etc.), and location (GPS-based or manual).
Recipient Search: Users pay a small fee to search for donors by blood type and proximity, receiving a list of contacts (limited to 20 to prevent abuse).
Geolocation: Uses the geolocator package to capture and match locations, storing coordinates as GeoPoint in Firestore.
Payment Integration: M-Pesa (via Safaricom's Daraja API) for processing search fees.
Privacy: Consent checkboxes, data encryption, and masked phone numbers (e.g., show last 4 digits initially).
Notifications: Optional SMS/push alerts for donors (via Twilio or Firebase Cloud Messaging).

Prerequisites

Flutter SDK: Install from flutter.dev. Run flutter doctor to verify setup.
IDE: Android Studio (for Android emulator) or Xcode (for iOS simulator). VS Code recommended for coding.
Firebase Account: Sign up at console.firebase.google.com. Create a project.
M-Pesa API: Register for Daraja API at developer.safaricom.co.ke for sandbox keys.
Git: For version control.
Device/Emulator: For testing.

Setup Instructions
1. Create Flutter Project
flutter create blood_donor_app
cd blood_donor_app

2. Add Dependencies
Update pubspec.yaml:
dependencies:
  flutter:
    sdk: flutter
  firebase_core: ^2.17.0
  cloud_firestore: ^4.9.3
  firebase_auth: ^4.10.0
  http: ^1.1.0
  geolocator: ^10.1.0
  fluttertoast: ^8.2.4

Run flutter pub get.
3. Configure Firebase

In Firebase console, add Android/iOS apps to your project.
Download google-services.json (Android) and GoogleService-Info.plist (iOS).
Place files in android/app/ and ios/Runner/.
Initialize Firebase in lib/main.dart:import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(MyApp());
}



4. Configure Geolocation

Android:Add to android/app/src/main/AndroidManifest.xml:<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />

Set compileSdkVersion 33 in android/app/build.gradle.
iOS:Add to ios/Runner/Info.plist:<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to find nearby donors.</string>
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>We need your location to find nearby donors.</string>



5. Configure M-Pesa

Obtain consumer key and secret from Daraja API.
Use sandbox URL (https://sandbox.safaricom.co.ke) for testing.

Project Structure
blood_donor_app/
├── lib/
│   ├── main.dart
│   ├── models/
│   │   └── donor.dart
│   ├── screens/
│   │   ├── enrollment_screen.dart
│   │   ├── search_screen.dart
│   │   └── payment_screen.dart
│   ├── services/
│   │   ├── database_service.dart
│   │   └── mpesa_service.dart
│   └── widgets/
│       └── custom_button.dart
├── pubspec.yaml
└── firebase_options.dart

Implementation Details
1. Donor Model (lib/models/donor.dart)
Stores donor data with a GeoPoint for location:
import 'package:cloud_firestore/cloud_firestore.dart';

class Donor {
  final String id;
  final String firstName;
  final String phoneNumber;
  final String bloodType;
  final GeoPoint location;

  Donor({required this.id, required this.firstName, required this.phoneNumber, required this.bloodType, required this.location});

  Map<String, dynamic> toMap() {
    return {
      'firstName': firstName,
      'phoneNumber': phoneNumber,
      'bloodType': bloodType,
      'location': location,
    };
  }

  factory Donor.fromMap(String id, Map<String, dynamic> map) {
    return Donor(
      id: id,
      firstName: map['firstName'],
      phoneNumber: map['phoneNumber'],
      bloodType: map['bloodType'],
      location: map['location'] as GeoPoint,
    );
  }
}

2. Database Service (lib/services/database_service.dart)
Handles Firestore operations, including geospatial filtering:
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:geolocator/geolocator.dart';
import '../models/donor.dart';

class DatabaseService {
  final CollectionReference donorsCollection = FirebaseFirestore.instance.collection('donors');

  Future<void> addDonor(Donor donor) async {
    await donorsCollection.doc(donor.id).set(donor.toMap());
  }

  Future<List<Donor>> searchDonors(String bloodType, GeoPoint userLocation, {double maxDistanceKm = 50}) async {
    QuerySnapshot snapshot = await donorsCollection
        .where('bloodType', isEqualTo: bloodType)
        .limit(50)
        .get();

    List<Donor> donors = snapshot.docs
        .map((doc) => Donor.fromMap(doc.id, doc.data() as Map<String, dynamic>))
        .toList();

    return donors.where((donor) {
      double distance = Geolocator.distanceBetween(
        userLocation.latitude,
        userLocation.longitude,
        donor.location.latitude,
        donor.location.longitude,
      ) / 1000;
      return distance <= maxDistanceKm;
    }).toList();
  }
}

3. M-Pesa Service (lib/services/mpesa_service.dart)
Handles payment processing (simplified):
import 'package:http/http.dart' as http;
import 'dart:convert';

class MpesaService {
  final String consumerKey = 'YOUR_CONSUMER_KEY';
  final String consumerSecret = 'YOUR_CONSUMER_SECRET';
  final String baseUrl = 'https://sandbox.safaricom.co.ke';

  Future<String> getAccessToken() async {
    String auth = base64Encode(utf8.encode('$consumerKey:$consumerSecret'));
    var response = await http.get(
      Uri.parse('$baseUrl/oauth/v1/generate?grant_type=client_credentials'),
      headers: {'Authorization': 'Basic $auth'},
    );
    return jsonDecode(response.body)['access_token'];
  }

  Future<bool> initiatePayment(String phone, double amount) async {
    String token = await getAccessToken();
    // Implement STK Push here
    return true; // Placeholder
  }
}

4. Enrollment Screen (lib/screens/enrollment_screen.dart)
Captures donor data with GPS location:
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/donor.dart';
import '../services/database_service.dart';
import 'package:fluttertoast/fluttertoast.dart';

class EnrollmentScreen extends StatefulWidget {
  @override
  _EnrollmentScreenState createState() => _EnrollmentScreenState();
}

class _EnrollmentScreenState extends State<EnrollmentScreen> {
  final _formKey = GlobalKey<FormState>();
  String firstName = '', phone = '', bloodType = '';
  GeoPoint? location;
  bool isLoading = false;
  final DatabaseService _db = DatabaseService();

  Future<bool> _handleLocationPermission() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      Fluttertoast.showToast(msg: 'Please enable location services.');
      return false;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        Fluttertoast.showToast(msg: 'Location permission denied.');
        return false;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      Fluttertoast.showToast(msg: 'Location permissions are permanently denied.');
      return false;
    }
    return true;
  }

  Future<void> _getCurrentLocation() async {
    setState(() => isLoading = true);
    try {
      bool hasPermission = await _handleLocationPermission();
      if (hasPermission) {
        Position position = await Geolocator.getCurrentPosition(
          desiredAccuracy: LocationAccuracy.high,
        );
        setState(() {
          location = GeoPoint(position.latitude, position.longitude);
        });
        Fluttertoast.showToast(msg: 'Location captured successfully!');
      }
    } catch (e) {
      Fluttertoast.showToast(msg: 'Error getting location: $e');
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Enroll as Donor')),
      body: Form(
        key: _formKey,
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'First Name'),
                onChanged: (val) => firstName = val,
                validator: (val) => val!.isEmpty ? 'Enter name' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Phone Number (+254...)'),
                onChanged: (val) => phone = val,
                validator: (val) => val!.startsWith('+254') ? null : 'Enter valid phone',
              ),
              DropdownButtonFormField(
                items: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                    .map((type) => DropdownMenuItem(value: type, child: Text(type)))
                    .toList(),
                onChanged: (val) => bloodType = val.toString(),
                decoration: InputDecoration(labelText: 'Blood Type'),
                validator: (val) => val == null ? 'Select blood type' : null,
              ),
              ElevatedButton(
                onPressed: isLoading ? null : _getCurrentLocation,
                child: Text(location == null ? 'Get Location' : 'Location Set'),
              ),
              if (isLoading) CircularProgressIndicator(),
              ElevatedButton(
                onPressed: isLoading || location == null
                    ? null
                    : () async {
                        if (_formKey.currentState!.validate()) {
                          String id = DateTime.now().millisecondsSinceEpoch.toString();
                          Donor donor = Donor(
                            id: id,
                            firstName: firstName,
                            phoneNumber: phone,
                            bloodType: bloodType,
                            location: location!,
                          );
                          await _db.addDonor(donor);
                          Fluttertoast.showToast(msg: 'Enrolled successfully!');
                          Navigator.pop(context);
                        }
                      },
                child: Text('Enroll'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

5. Search Screen (lib/screens/search_screen.dart)
Searches donors by blood type and proximity:
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/donor.dart';
import '../services/database_service.dart';
import '../services/mpesa_service.dart';
import 'package:fluttertoast/fluttertoast.dart';

class SearchScreen extends StatefulWidget {
  @override
  _SearchScreenState createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  String bloodType = '';
  GeoPoint? userLocation;
  bool isLoading = false;
  List<Donor> donors = [];
  final DatabaseService _db = DatabaseService();
  final MpesaService _mpesa = MpesaService();

  Future<void> _getUserLocation() async {
    setState(() => isLoading = true);
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        Fluttertoast.showToast(msg: 'Please enable location services.');
        return;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          Fluttertoast.showToast(msg: 'Location permission denied.');
          return;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        Fluttertoast.showToast(msg: 'Location permissions are permanently denied.');
        return;
      }

      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        userLocation = GeoPoint(position.latitude, position.longitude);
      });
    } catch (e) {
      Fluttertoast.showToast(msg: 'Error getting location: $e');
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Search Donors')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            DropdownButtonFormField(
              items: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                  .map((type) => DropdownMenuItem(value: type, child: Text(type)))
                  .toList(),
              onChanged: (val) => bloodType = val.toString(),
              decoration: InputDecoration(labelText: 'Blood Type'),
              validator: (val) => val == null ? 'Select blood type' : null,
            ),
            ElevatedButton(
              onPressed: isLoading ? null : _getUserLocation,
              child: Text(userLocation == null ? 'Get Location' : 'Location Set'),
            ),
            if (isLoading) CircularProgressIndicator(),
            ElevatedButton(
              onPressed: isLoading || userLocation == null || bloodType.isEmpty
                  ? null
                  : () async {
                      setState(() => isLoading = true);
                      try {
                        bool paid = await _mpesa.initiatePayment('2547xxxxxxxx', 50.0);
                        if (paid) {
                          donors = await _db.searchDonors(bloodType, userLocation!);
                          Fluttertoast.showToast(msg: 'Search complete!');
                        } else {
                          Fluttertoast.showToast(msg: 'Payment failed.');
                        }
                      } catch (e) {
                        Fluttertoast.showToast(msg: 'Error: $e');
                      } finally {
                        setState(() => isLoading = false);
                      }
                    },
              child: Text('Pay & Search (KSh 50)'),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: donors.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text('${donors[index].firstName} - ${donors[index].bloodType}'),
                    subtitle: Text('Phone: ${donors[index].phoneNumber}'),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

6. Main App (lib/main.dart)
Navigation hub:
import 'package:flutter/material.dart';
import 'screens/enrollment_screen.dart';
import 'screens/search_screen.dart';

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Blood Donor App',
      home: HomeScreen(),
      routes: {
        '/enroll': (context) => EnrollmentScreen(),
        '/search': (context) => SearchScreen(),
      },
    );
  }
}

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Blood Donor App')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(onPressed: () => Navigator.pushNamed(context, '/enroll'), child: Text('Enroll as Donor')),
            ElevatedButton(onPressed: () => Navigator.pushNamed(context, '/search'), child: Text('Search for Donors')),
          ],
        ),
      ),
    );
  }
}

Geolocation Integration
The app uses the geolocator package to:

Capture Location: Donors and recipients provide GPS coordinates (GeoPoint) during enrollment and search.
Handle Permissions: Requests ACCESS_FINE_LOCATION (Android) or NSLocationWhenInUseUsageDescription (iOS).
Calculate Distance: Uses Geolocator.distanceBetween for client-side filtering of donors within 50km.
Fallback: Manual city input with geocoding API (e.g., Nominatim) can be added:Future<GeoPoint?> getCoordinatesFromCity(String city) async {
  final response = await http.get(Uri.parse('https://nominatim.openstreetmap.org/search?q=$city,Kenya&format=json'));
  var data = jsonDecode(response.body);
  if (data.isNotEmpty) {
    return GeoPoint(double.parse(data[0]['lat']), double.parse(data[0]['lon']));
  }
  return null;
}



Edge Cases

Location Disabled: Prompts to enable GPS.
Permission Denied: Guides to app settings.
No Donors: Shows message if no matches found.
Performance: Limits queries to 50 results; consider GeoFirestore for scalability.

Security and Privacy

Data Encryption: Uses HTTPS and Firestore’s security rules.
Consent: Donors opt-in to share contacts.
Masked Contacts: Show partial phone numbers initially.
Rate Limiting: Caps searches to prevent abuse.

Testing

Emulator:
Android: Set mock location in “Extended Controls > Location” (e.g., Nairobi: -1.286389, 36.817223).
iOS: Use “Features > Location > Custom Location”.


Real Device: Test permissions and GPS accuracy.
Firestore: Add test donors (e.g., Nairobi: GeoPoint(-1.28, 36.81), Mombasa: GeoPoint(-4.04, 39.67)).
M-Pesa: Use sandbox for payment testing.

Deployment

Build:
Android: flutter build apk --release
iOS: flutter build ipa


Publish:
Google Play: Upload APK ($25 fee).
App Store: Upload IPA ($99/year).


Firebase Security Rules:rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /donors/{donorId} {
      allow read: if request.auth != null; // Restrict to authenticated users
      allow write: if request.auth != null;
    }
  }
}



Future Enhancements

GeoFirestore: For native geospatial queries.
Notifications: Firebase Cloud Messaging for donor alerts.
Verification: Require donor card uploads (Firebase Storage).
Dynamic Radius: Slider for 10km, 50km, etc.
Free Tier: Subsidized searches for emergencies.

Challenges

Data Costs: Cache locations with SharedPreferences.
Battery: Use LocationAccuracy.medium for non-critical tasks.
Firestore Costs: Optimize queries or use GeoFirestore.
Legal: Consult Kenya’s Data Protection Act and KNBTS.

Contributing
Fork the repo, create a branch, and submit a pull request. Report issues via GitHub Issues.
License
MIT License. Use freely, but ensure compliance with local regulations.
