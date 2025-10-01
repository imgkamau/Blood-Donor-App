# Blood Donor App - Deployment Guide

## Backend Deployment Options

Your backend is working perfectly with RDS! Now you need to deploy it to make it accessible to your Flutter app.

### Option 1: AWS Elastic Beanstalk (Recommended - Easiest)

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB:**
   ```bash
   cd backend
   eb init
   ```

3. **Create environment:**
   ```bash
   eb create blood-donor-backend
   ```

4. **Deploy:**
   ```bash
   eb deploy
   ```

5. **Get URL:**
   ```bash
   eb status
   ```

### Option 2: Railway (Simple & Fast)

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select the `backend` folder
4. Add environment variable: `DATABASE_URL=postgresql://postgres:YourSecurePassword123!@blood-donor-db.cfu6ig0486fv.eu-west-3.rds.amazonaws.com:5432/postgres`
5. Deploy automatically

### Option 3: Render (Free Tier Available)

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `DATABASE_URL=postgresql://postgres:YourSecurePassword123!@blood-donor-db.cfu6ig0486fv.eu-west-3.rds.amazonaws.com:5432/postgres`

## After Backend Deployment

1. **Update Flutter App Configuration:**
   ```dart
   // In lib/config/app_config.dart
   static const String apiBaseUrl = 'https://your-actual-backend-url.com/api/v1';
   ```

2. **Update WebSocket URL:**
   ```dart
   // In lib/services/websocket_service.dart
   final String wsUrl = AppConfig.isDevelopment
       ? 'ws://10.0.2.2:8000/ws'
       : 'wss://your-actual-backend-url.com/ws';
   ```

3. **Build New AAB:**
   ```bash
   flutter build appbundle --release
   ```

## Testing Checklist

- [ ] Backend deployed and accessible
- [ ] Health endpoint working: `https://your-backend-url.com/health`
- [ ] Donor creation working
- [ ] Donor search working
- [ ] WebSocket connection working
- [ ] Flutter app updated with correct URLs
- [ ] New AAB built and tested

## Current Status

✅ **RDS Database**: Working perfectly
✅ **Backend API**: All endpoints tested and working
✅ **Flutter App**: Ready for production
⏳ **Backend Deployment**: Needs to be deployed to cloud
⏳ **App Configuration**: Needs backend URL update

## Next Steps

1. Deploy your backend using one of the options above
2. Update the Flutter app configuration with the deployed backend URL
3. Build and upload the final AAB to Google Play Console
