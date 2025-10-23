# Mobile Access Guide - Waste Sorting App

This guide explains how to access the waste sorting app from your mobile phone.

## Why HTTPS is Required

Modern browsers (especially on mobile) require **HTTPS** to access the camera for security reasons. HTTP only works on `localhost`.

## Setup Steps

### Step 1: Generate SSL Certificate (One-time)

In WSL/Linux terminal:

```bash
cd /home/danny/repos/waste-sorting-app
./generate_cert.sh
```

This creates a self-signed certificate in the `certs/` folder.

### Step 2: Set Up Windows Port Forwarding (WSL Users Only)

**Open PowerShell as Administrator** and run:

```powershell
cd \\wsl$\Ubuntu\home\danny\repos\waste-sorting-app
.\setup_windows_portforward.ps1
```

This will:
- Configure port forwarding from Windows to WSL
- Add Windows Firewall rule
- Display your Windows IP address

### Step 3: Start the Application

In WSL/Linux terminal:

```bash
./run.sh
```

You should see:
```
============================================================
Waste Sorting Application is running!
============================================================
Access from this computer: https://localhost:5000
Access from mobile phone: https://192.168.1.4:5000
============================================================
```

## Accessing from Mobile

### URL Format

Use the HTTPS URL shown when the app starts:
```
https://192.168.1.4:5000
```

Replace `192.168.1.4` with your actual Windows IP address.

### Accept the Security Certificate

Since we're using a self-signed certificate, you'll see a security warning:

#### On iPhone/iPad (Safari):
1. You'll see "This Connection Is Not Private"
2. Tap "Show Details"
3. Tap "visit this website"
4. Tap "Visit Website" again to confirm

#### On Android (Chrome):
1. You'll see "Your connection is not private"
2. Tap "Advanced"
3. Tap "Proceed to [IP address] (unsafe)"

#### On Desktop Browser:
1. You'll see "Your connection is not private" or similar
2. Click "Advanced"
3. Click "Proceed to [IP address] (unsafe)" or "Accept the risk and continue"

**Note:** This is safe because you generated the certificate yourself and are only using it on your local network.

## Troubleshooting

### "Unable to access camera" Error

**Symptom:** Error message says "can't access property getUserMedia"

**Solution:** Make sure you're using **HTTPS**, not HTTP:
- ✅ Correct: `https://192.168.1.4:5000`
- ❌ Wrong: `http://192.168.1.4:5000`

### Cannot Access from Mobile

**Check these:**

1. **Same WiFi Network**
   - Verify mobile and laptop are on the same WiFi
   - Don't use mobile data

2. **Port Forwarding (WSL Users)**
   - Run `setup_windows_portforward.ps1` in PowerShell as Admin
   - Check it completed successfully

3. **Verify Port Forwarding**
   In PowerShell:
   ```powershell
   netsh interface portproxy show v4tov4
   ```

   Should show:
   ```
   Listen on ipv4:             Connect to ipv4:
   Address         Port        Address         Port
   --------------- ----------  --------------- ----------
   0.0.0.0         5000        172.23.89.69    5000
   ```

4. **Windows Firewall**
   - Make sure port 5000 is allowed
   - The setup script should have added the rule automatically
   - To check in PowerShell:
     ```powershell
     Get-NetFirewallRule -DisplayName "Waste Sorting App"
     ```

5. **Test from Laptop First**
   - Try accessing `https://192.168.1.4:5000` from your laptop browser first
   - If it works on laptop but not mobile, it's likely a firewall issue

### Certificate Expired

If you see "certificate expired" after 365 days:

```bash
# Delete old certificate
rm -rf certs/

# Generate new one
./generate_cert.sh
```

### Port 5000 Already in Use

```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process (replace PID with actual process ID)
kill -9 PID

# Or use a different port by editing app.py
```

## Remove Port Forwarding (When Done)

To remove port forwarding in PowerShell:

```powershell
netsh interface portproxy delete v4tov4 listenport=5000 listenaddress=0.0.0.0
Remove-NetFirewallRule -DisplayName "Waste Sorting App"
```

## Quick Reference

| Access From | URL |
|-------------|-----|
| Laptop (WSL/Linux) | `https://localhost:5000` |
| Laptop (Windows) | `https://localhost:5000` or `https://192.168.1.4:5000` |
| Mobile Phone | `https://192.168.1.4:5000` |

**Important:** Always use `https://` (not `http://`) for camera access!
