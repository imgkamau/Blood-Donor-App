@echo off
echo Creating release-signed AAB for Blood Donor App...

REM Navigate to project directory
cd /d "C:\Users\gwaru\Documents\GitHub\Blood-Donor-App"

REM Create keystore (if it doesn't exist)
if not exist "keystore\blood-donor-keystore.jks" (
    echo Creating keystore...
    keytool -genkey -v -keystore keystore\blood-donor-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias blood-donor-key
)

REM Build release AAB
echo Building release AAB...
C:\Users\gwaru\dev\flutter\bin\flutter.bat build appbundle --release

echo.
echo AAB created successfully!
echo Location: build\app\outputs\bundle\release\app-release.aab
echo.
echo Next steps:
echo 1. Upload app-release.aab to Google Play Console
echo 2. Complete your app listing
echo 3. Submit for review
echo.
pause
