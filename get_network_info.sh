#!/bin/bash

echo "========================================"
echo "Network Information for Waste Sorting App"
echo "========================================"
echo ""

# Get WSL IP
WSL_IP=$(hostname -I | awk '{print $1}')
echo "WSL IP Address: $WSL_IP"

# Try to get Windows host IP
if command -v powershell.exe &> /dev/null; then
    echo ""
    echo "Detecting Windows Host IP..."
    WINDOWS_IP=$(powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi' -ErrorAction SilentlyContinue).IPAddress" 2>/dev/null | tr -d '\r')

    if [ -z "$WINDOWS_IP" ]; then
        # Try Ethernet if Wi-Fi not found
        WINDOWS_IP=$(powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Ethernet' -ErrorAction SilentlyContinue).IPAddress" 2>/dev/null | tr -d '\r')
    fi

    if [ -z "$WINDOWS_IP" ]; then
        # Get all network adapters
        echo ""
        echo "Available Network Adapters:"
        powershell.exe -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {(\$_.IPAddress -notlike '127.*') -and (\$_.IPAddress -notlike '169.254.*')} | Select-Object IPAddress, InterfaceAlias | Format-Table -AutoSize" 2>/dev/null
    else
        echo "Windows Host IP: $WINDOWS_IP"
    fi
fi

echo ""
echo "========================================"
echo "Access Instructions:"
echo "========================================"
echo ""
echo "OPTION 1 - From WSL/Linux on this computer:"
echo "  http://localhost:5000"
echo "  http://$WSL_IP:5000"
echo ""

if [ ! -z "$WINDOWS_IP" ]; then
    echo "OPTION 2 - From mobile phone (same WiFi):"
    echo "  http://$WINDOWS_IP:5000"
    echo ""
    echo "⚠️  IMPORTANT: You need to set up port forwarding in Windows!"
    echo "   Run this command in Windows PowerShell (as Administrator):"
    echo ""
    echo "   netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=$WSL_IP"
    echo ""
    echo "   To remove port forwarding later:"
    echo "   netsh interface portproxy delete v4tov4 listenport=5000 listenaddress=0.0.0.0"
    echo ""
    echo "   To check Windows Firewall (you may need to allow port 5000):"
    echo "   New-NetFirewallRule -DisplayName 'Waste Sorting App' -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow"
else
    echo "OPTION 2 - From mobile phone:"
    echo "  Could not detect Windows IP automatically."
    echo "  Please run 'ipconfig' in Windows Command Prompt"
    echo "  and look for your WiFi adapter's IPv4 address"
fi

echo ""
echo "========================================"
