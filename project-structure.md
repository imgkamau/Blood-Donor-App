# Blood Donor App - Development Structure Tree

## Project Overview
Flutter-based mobile application connecting blood recipients with nearby donors in Kenya, featuring payment integration, geolocation services, and privacy controls.

## Development Phases & Structure

```
Blood-Donor-App/
├── 📱 FLUTTER MOBILE APP (Phase 1-3)
│   ├── lib/
│   │   ├── main.dart                          # App entry point & navigation
│   │   ├── config/
│   │   │   ├── app_config.dart                # App constants & settings
│   │   │   ├── database_config.dart           # PostgreSQL connection config
│   │   │   └── api_config.dart                # M-Pesa API configuration
│   │   ├── models/
│   │   │   ├── donor.dart                     # Donor data model
│   │   │   ├── recipient.dart                 # Recipient data model
│   │   │   ├── payment.dart                   # Payment transaction model
│   │   │   └── location.dart                  # Location/GPS model
│   │   ├── screens/
│   │   │   ├── auth/
│   │   │   │   ├── login_screen.dart          # User authentication
│   │   │   │   └── register_screen.dart       # User registration
│   │   │   ├── donor/
│   │   │   │   ├── enrollment_screen.dart     # Donor registration
│   │   │   │   ├── donor_profile_screen.dart  # Donor profile management
│   │   │   │   └── donor_dashboard.dart       # Donor dashboard
│   │   │   ├── recipient/
│   │   │   │   ├── search_screen.dart         # Search for donors
│   │   │   │   ├── results_screen.dart        # Display search results
│   │   │   │   └── recipient_dashboard.dart   # Recipient dashboard
│   │   │   ├── payment/
│   │   │   │   ├── payment_screen.dart        # M-Pesa payment interface
│   │   │   │   ├── payment_success.dart       # Payment confirmation
│   │   │   │   └── payment_history.dart       # Transaction history
│   │   │   ├── location/
│   │   │   │   ├── location_permission.dart   # Location permission handling
│   │   │   │   ├── map_screen.dart            # Interactive map view
│   │   │   │   └── manual_location.dart       # Manual location input
│   │   │   └── common/
│   │   │       ├── home_screen.dart           # Main navigation hub
│   │   │       ├── settings_screen.dart       # App settings
│   │   │       ├── about_screen.dart          # App information
│   │   │       └── privacy_screen.dart        # Privacy policy & consent
│   │   ├── services/
│   │   │   ├── database/
│   │   │   │   ├── database_service.dart      # PostgreSQL operations
│   │   │   │   ├── donor_service.dart         # Donor CRUD operations
│   │   │   │   ├── recipient_service.dart     # Recipient operations
│   │   │   │   └── location_service.dart      # Location-based queries
│   │   │   ├── payment/
│   │   │   │   ├── mpesa_service.dart         # M-Pesa integration
│   │   │   │   ├── payment_validation.dart    # Payment verification
│   │   │   │   └── transaction_service.dart   # Transaction management
│   │   │   ├── location/
│   │   │   │   ├── geolocation_service.dart   # GPS & location handling
│   │   │   │   ├── geocoding_service.dart     # Address to coordinates
│   │   │   │   └── distance_calculator.dart   # Distance calculations
│   │   │   ├── notification/
│   │   │   │   ├── sms_service.dart           # SMS notifications
│   │   │   │   ├── push_notification.dart     # Push notifications
│   │   │   │   └── email_service.dart         # Email notifications
│   │   │   └── security/
│   │   │       ├── encryption_service.dart    # Data encryption
│   │   │       ├── auth_service.dart          # Authentication
│   │   │       └── privacy_service.dart       # Privacy controls
│   │   ├── widgets/
│   │   │   ├── common/
│   │   │   │   ├── custom_button.dart         # Reusable button component
│   │   │   │   ├── custom_textfield.dart      # Custom input fields
│   │   │   │   ├── loading_widget.dart        # Loading indicators
│   │   │   │   ├── error_widget.dart          # Error display components
│   │   │   │   └── success_widget.dart        # Success message components
│   │   │   ├── donor/
│   │   │   │   ├── donor_card.dart            # Donor profile card
│   │   │   │   ├── blood_type_selector.dart   # Blood type dropdown
│   │   │   │   └── donor_list_item.dart       # Donor list item
│   │   │   ├── location/
│   │   │   │   ├── location_picker.dart       # Interactive location picker
│   │   │   │   ├── distance_indicator.dart    # Distance display
│   │   │   │   └── map_widget.dart            # Embedded map component
│   │   │   └── payment/
│   │   │       ├── payment_form.dart          # Payment input form
│   │   │       ├── amount_selector.dart       # Amount selection
│   │   │       └── payment_status.dart        # Payment status display
│   │   ├── utils/
│   │   │   ├── constants.dart                 # App constants
│   │   │   ├── validators.dart                # Form validation
│   │   │   ├── helpers.dart                   # Utility functions
│   │   │   ├── formatters.dart                # Data formatters
│   │   │   └── permissions.dart               # Permission handling
│   │   └── themes/
│   │       ├── app_theme.dart                 # App color scheme
│   │       ├── text_styles.dart               # Typography
│   │       └── component_themes.dart          # Component styling
│   ├── assets/
│   │   ├── images/
│   │   │   ├── logo.png                       # App logo
│   │   │   ├── blood_drop.png                 # Blood drop icon
│   │   │   ├── location_pin.png               # Location icon
│   │   │   └── mpesa_logo.png                 # M-Pesa logo
│   │   ├── icons/
│   │   │   ├── donor_icon.svg                 # Donor icon
│   │   │   ├── recipient_icon.svg             # Recipient icon
│   │   │   └── emergency_icon.svg             # Emergency icon
│   │   └── fonts/
│   │       └── custom_fonts/                  # Custom font files
│   ├── android/
│   │   ├── app/
│   │   │   ├── src/main/
│   │   │   │   ├── AndroidManifest.xml        # Android permissions
│   │   │   │   └── res/                       # Android resources
│   │   │   └── build.gradle                   # Android build config
│   │   └── build.gradle                       # Project build config
│   ├── ios/
│   │   ├── Runner/
│   │   │   ├── Info.plist                     # iOS permissions
│   │   │   └── Assets.xcassets/               # iOS assets
│   │   └── Runner.xcodeproj/                  # iOS project
│   └── pubspec.yaml                           # Flutter dependencies
│
├── 🗄️ BACKEND API (Phase 2-4)
│   ├── backend/
│   │   ├── src/
│   │   │   ├── main.py                        # FastAPI application entry
│   │   │   ├── config/
│   │   │   │   ├── database.py                # PostgreSQL configuration
│   │   │   │   ├── settings.py                # Environment settings
│   │   │   │   └── security.py                # Security configurations
│   │   │   ├── models/
│   │   │   │   ├── donor.py                   # Donor SQLAlchemy model
│   │   │   │   ├── recipient.py               # Recipient SQLAlchemy model
│   │   │   │   ├── payment.py                 # Payment SQLAlchemy model
│   │   │   │   ├── location.py                # Location SQLAlchemy model
│   │   │   │   └── user.py                    # User SQLAlchemy model
│   │   │   ├── schemas/
│   │   │   │   ├── donor_schema.py            # Pydantic schemas for donors
│   │   │   │   ├── recipient_schema.py        # Pydantic schemas for recipients
│   │   │   │   ├── payment_schema.py          # Pydantic schemas for payments
│   │   │   │   └── location_schema.py         # Pydantic schemas for locations
│   │   │   ├── api/
│   │   │   │   ├── v1/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── donors.py              # Donor API endpoints
│   │   │   │   │   ├── recipients.py          # Recipient API endpoints
│   │   │   │   │   ├── payments.py            # Payment API endpoints
│   │   │   │   │   ├── locations.py           # Location API endpoints
│   │   │   │   │   └── auth.py                # Authentication endpoints
│   │   │   │   └── __init__.py
│   │   │   ├── core/
│   │   │   │   ├── database.py                # Database connection
│   │   │   │   ├── security.py                # JWT & password hashing
│   │   │   │   ├── dependencies.py            # FastAPI dependencies
│   │   │   │   └── exceptions.py              # Custom exceptions
│   │   │   ├── services/
│   │   │   │   ├── donor_service.py           # Donor business logic
│   │   │   │   ├── recipient_service.py       # Recipient business logic
│   │   │   │   ├── payment_service.py         # Payment processing
│   │   │   │   ├── location_service.py        # Location calculations
│   │   │   │   ├── mpesa_service.py           # M-Pesa integration
│   │   │   │   ├── notification_service.py    # SMS/Email notifications
│   │   │   │   └── encryption_service.py      # Data encryption
│   │   │   └── utils/
│   │   │       ├── validators.py              # Data validation
│   │   │       ├── helpers.py                 # Utility functions
│   │   │       ├── geolocation.py             # GPS calculations
│   │   │       └── formatters.py              # Data formatting
│   │   ├── migrations/
│   │   │   ├── versions/                      # Alembic migration files
│   │   │   └── alembic.ini                    # Alembic configuration
│   │   ├── tests/
│   │   │   ├── test_donors.py                 # Donor API tests
│   │   │   ├── test_recipients.py             # Recipient API tests
│   │   │   ├── test_payments.py               # Payment API tests
│   │   │   └── test_locations.py              # Location API tests
│   │   ├── requirements.txt                   # Python dependencies
│   │   ├── Dockerfile                         # Container configuration
│   │   └── docker-compose.yml                 # Multi-service setup
│
├── 🗃️ DATABASE (Phase 1-2)
│   ├── database/
│   │   ├── init/
│   │   │   ├── 01_create_tables.sql           # Initial table creation
│   │   │   ├── 02_insert_sample_data.sql      # Sample data for testing
│   │   │   └── 03_create_indexes.sql          # Performance indexes
│   │   ├── migrations/
│   │   │   ├── 001_add_user_verification.sql  # User verification fields
│   │   │   ├── 002_add_payment_tracking.sql   # Payment tracking fields
│   │   │   └── 003_add_notification_prefs.sql # Notification preferences
│   │   ├── schemas/
│   │   │   ├── donors.sql                     # Donor table schema
│   │   │   ├── recipients.sql                 # Recipient table schema
│   │   │   ├── payments.sql                   # Payment table schema
│   │   │   ├── locations.sql                  # Location table schema
│   │   │   └── users.sql                      # User table schema
│   │   └── seeds/
│   │       ├── kenya_cities.sql               # Kenya cities data
│   │       ├── blood_types.sql                # Blood type definitions
│   │       └── sample_donors.sql              # Sample donor data
│
├── 🔧 DEVELOPMENT TOOLS (Phase 1-5)
│   ├── scripts/
│   │   ├── setup_database.sh                  # Database setup script
│   │   ├── run_migrations.sh                  # Migration runner
│   │   ├── seed_data.sh                       # Data seeding script
│   │   ├── build_app.sh                       # App build script
│   │   └── deploy.sh                          # Deployment script
│   ├── docs/
│   │   ├── api_documentation.md               # API documentation
│   │   ├── database_schema.md                 # Database design
│   │   ├── deployment_guide.md                # Deployment instructions
│   │   ├── testing_guide.md                   # Testing procedures
│   │   └── user_manual.md                     # User guide
│   ├── tests/
│   │   ├── unit/                              # Unit tests
│   │   ├── integration/                       # Integration tests
│   │   ├── e2e/                               # End-to-end tests
│   │   └── performance/                       # Performance tests
│   └── tools/
│       ├── postman_collection.json            # API testing collection
│       ├── database_diagram.drawio            # Database ERD
│       └── app_mockups.fig                    # UI/UX mockups
│
└── 📋 CONFIGURATION FILES
    ├── .gitignore                             # Git ignore rules
    ├── .env.example                           # Environment variables template
    ├── docker-compose.yml                     # Development environment
    ├── nginx.conf                             # Web server configuration
    ├── ssl/                                   # SSL certificates
    └── logs/                                  # Application logs
```

## Development Phases

### Phase 1: Foundation Setup (Week 1-2)
- [ ] Flutter project initialization
- [ ] PostgreSQL database setup
- [ ] Basic project structure
- [ ] Development environment configuration
- [ ] Git repository setup

### Phase 2: Core Backend (Week 3-4)
- [ ] FastAPI backend setup
- [ ] Database models and schemas
- [ ] Basic CRUD operations
- [ ] Authentication system
- [ ] API documentation

### Phase 3: Mobile App Core (Week 5-6)
- [ ] Flutter UI framework
- [ ] Navigation structure
- [ ] Basic screens implementation
- [ ] API integration
- [ ] State management setup

### Phase 4: Advanced Features (Week 7-8)
- [ ] Geolocation integration
- [ ] M-Pesa payment integration
- [ ] Search and filtering
- [ ] Privacy controls
- [ ] Notification system

### Phase 5: Testing & Deployment (Week 9-10)
- [ ] Unit and integration testing
- [ ] Performance optimization
- [ ] Security audit
- [ ] Production deployment
- [ ] App store preparation

## Key Technologies

### Frontend (Flutter)
- **Framework**: Flutter 3.x
- **State Management**: Provider/Riverpod
- **HTTP Client**: Dio
- **Location**: Geolocator
- **Maps**: Google Maps/OpenStreetMap
- **UI Components**: Material Design 3

### Backend (Python)
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: JWT tokens
- **API Documentation**: Swagger/OpenAPI
- **Payment**: M-Pesa Daraja API
- **Notifications**: Twilio SMS

### Database (PostgreSQL)
- **Version**: PostgreSQL 14+
- **Extensions**: PostGIS (for geospatial queries)
- **Connection**: psycopg2
- **Migrations**: Alembic

### Infrastructure
- **Containerization**: Docker
- **Web Server**: Nginx
- **SSL**: Let's Encrypt
- **Monitoring**: Basic logging

## Database Schema Overview

```sql
-- Core Tables
users (id, email, phone, password_hash, created_at, updated_at)
donors (id, user_id, first_name, blood_type, location, is_verified, created_at)
recipients (id, user_id, search_count, last_search, created_at)
payments (id, recipient_id, amount, mpesa_receipt, status, created_at)
locations (id, user_id, latitude, longitude, address, created_at)
notifications (id, user_id, type, message, sent_at, status)
```

## Security Considerations

1. **Data Encryption**: All sensitive data encrypted at rest
2. **API Security**: JWT authentication, rate limiting
3. **Privacy Controls**: Consent management, data masking
4. **Payment Security**: PCI compliance, secure M-Pesa integration
5. **Location Privacy**: Optional location sharing, data retention policies

## Next Steps

1. **Confirm Requirements**: Review and approve this structure
2. **Environment Setup**: Configure development environment
3. **Database Design**: Finalize database schema
4. **API Specification**: Define API endpoints
5. **UI/UX Design**: Create app mockups and user flows

Would you like me to proceed with any specific phase or component?
