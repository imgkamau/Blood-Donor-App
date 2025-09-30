#!/bin/bash

echo "Finding your computer's IP address for mobile device connection..."
echo

echo "IPv4 Addresses:"
if command -v ip &> /dev/null; then
    ip addr show | grep "inet " | grep -v "127.0.0.1"
elif command -v ifconfig &> /dev/null; then
    ifconfig | grep "inet " | grep -v "127.0.0.1"
else
    echo "Could not find network interface command"
fi

echo
echo "Use one of these IP addresses in your Flutter app config"
echo "Example: http://192.168.1.100:8000/api/v1"
echo
echo "For Android Emulator: Use 10.0.2.2 (already configured)"
echo "For iOS Simulator: Use localhost (already configured)"
echo "For Physical Device: Use your computer's IP address above"
echo
