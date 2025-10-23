# PowerShell Script to Setup Port Forwarding for WSL2
# Run this in PowerShell as Administrator

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Waste Sorting App - WSL2 Port Forwarding Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Get WSL IP address
Write-Host "Getting WSL IP address..." -ForegroundColor Yellow
$wslIp = (wsl hostname -I).Trim().Split()[0]

if ([string]::IsNullOrEmpty($wslIp)) {
    Write-Host "ERROR: Could not detect WSL IP address" -ForegroundColor Red
    Write-Host "Make sure WSL is running" -ForegroundColor Red
    exit 1
}

Write-Host "WSL IP Address: $wslIp" -ForegroundColor Green

# Get Windows IP address
Write-Host ""
Write-Host "Getting Windows WiFi IP address..." -ForegroundColor Yellow
$windowsIp = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi" -ErrorAction SilentlyContinue).IPAddress

if ([string]::IsNullOrEmpty($windowsIp)) {
    Write-Host "WiFi adapter not found, trying Ethernet..." -ForegroundColor Yellow
    $windowsIp = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet" -ErrorAction SilentlyContinue).IPAddress
}

if ([string]::IsNullOrEmpty($windowsIp)) {
    Write-Host "WARNING: Could not auto-detect Windows IP" -ForegroundColor Yellow
    Write-Host "Available network adapters:" -ForegroundColor Yellow
    Get-NetIPAddress -AddressFamily IPv4 | Where-Object {($_.IPAddress -notlike "127.*") -and ($_.IPAddress -notlike "169.254.*")} | Select-Object IPAddress, InterfaceAlias | Format-Table -AutoSize
} else {
    Write-Host "Windows IP Address: $windowsIp" -ForegroundColor Green
}

# Remove existing port forwarding if it exists
Write-Host ""
Write-Host "Removing any existing port forwarding rules..." -ForegroundColor Yellow
netsh interface portproxy delete v4tov4 listenport=5000 listenaddress=0.0.0.0 2>$null

# Add port forwarding
Write-Host "Setting up port forwarding (port 5000)..." -ForegroundColor Yellow
$result = netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=$wslIp

if ($LASTEXITCODE -eq 0) {
    Write-Host "Port forwarding configured successfully!" -ForegroundColor Green
} else {
    Write-Host "Failed to configure port forwarding" -ForegroundColor Red
    Write-Host "Make sure you are running PowerShell as Administrator" -ForegroundColor Red
    exit 1
}

# Configure Windows Firewall
Write-Host ""
Write-Host "Configuring Windows Firewall..." -ForegroundColor Yellow

# Remove existing rule if it exists
Remove-NetFirewallRule -DisplayName "Waste Sorting App" -ErrorAction SilentlyContinue 2>$null

# Add new firewall rule
New-NetFirewallRule -DisplayName "Waste Sorting App" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Firewall rule added successfully!" -ForegroundColor Green
} else {
    Write-Host "Failed to add firewall rule" -ForegroundColor Red
}

# Display current port forwarding rules
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Current Port Forwarding Rules:" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
netsh interface portproxy show v4tov4

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access from this computer:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host ""

if (![string]::IsNullOrEmpty($windowsIp)) {
    Write-Host "Access from mobile phone (same WiFi):" -ForegroundColor Yellow
    Write-Host "  http://$windowsIp:5000" -ForegroundColor White
    Write-Host ""
}

Write-Host "To remove port forwarding later, run:" -ForegroundColor Yellow
Write-Host "  netsh interface portproxy delete v4tov4 listenport=5000 listenaddress=0.0.0.0" -ForegroundColor White
Write-Host ""
