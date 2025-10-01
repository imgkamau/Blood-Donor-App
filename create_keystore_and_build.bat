@echo off
echo Creating keystore and building signed AAB...

REM Create keystore directory
if not exist "keystore" mkdir keystore

REM Create keystore
echo Creating keystore...
keytool -genkey -v -keystore keystore\blood-donor-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias blood-donor-key -storepass BloodDonor2024! -keypass BloodDonor2024! -dname "CN=Blood Donor App, OU=Development, O=Blood Donor Kenya, L=Nairobi, ST=Nairobi, C=KE"

REM Create key.properties file
echo Creating key.properties...
echo storePassword=BloodDonor2024! > android\key.properties
echo keyPassword=BloodDonor2024! >> android\key.properties
echo keyAlias=blood-donor-key >> android\key.properties
echo storeFile=../keystore/blood-donor-keystore.jks >> android\key.properties

echo.
echo Keystore created successfully!
echo Password: BloodDonor2024!
echo Location: keystore\blood-donor-keystore.jks
echo.
echo Now building signed AAB...
C:\Users\gwaru\dev\flutter\bin\flutter.bat build appbundle --release

echo.
echo AAB created successfully!
echo Location: build\app\outputs\bundle\release\app-release.aab
echo.
echo IMPORTANT: Save your keystore password: BloodDonor2024!
echo You'll need this password every time you update your app!
echo.
pause
