@echo off
echo Finding your computer's IP address for mobile device connection...
echo.

echo IPv4 Addresses:
ipconfig | findstr "IPv4"

echo.
echo Use one of these IP addresses in your Flutter app config
echo Example: http://192.168.1.100:8000/api/v1
echo.
echo For Android Emulator: Use 10.0.2.2 (already configured)
echo For iOS Simulator: Use localhost (already configured)
echo For Physical Device: Use your computer's IP address above
echo.
pause
