# AI Waste Sorting Application

A web application that uses Anthropic's Claude vision model to classify waste into three categories: Organic, Inorganic, and Hazardous.

**[Live Demo](https://your-app.onrender.com)** (Replace with your deployed URL)

![Waste Sorting App](https://img.shields.io/badge/AI-Waste%20Sorting-green) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey) ![Claude](https://img.shields.io/badge/Anthropic-Claude-orange)

## 🚀 Deploy Online

Want to host this app online for free? See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step instructions!

Platforms supported:
- ✅ Render.com (Recommended - Free with HTTPS)
- ✅ Railway.app
- ✅ PythonAnywhere

## Features

- 📸 Camera capture directly from your device
- 🤖 AI-powered waste classification using Claude Vision
- 📱 Mobile-friendly interface
- 🌐 Works online or on local network
- ♻️ Four categories: Organic, Inorganic, Hazardous, Unknown
- 🔒 HTTPS support for secure camera access
- 🔄 Automatic retry on API errors
- ⚡ Fast Claude Haiku model

## Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- A laptop/computer to run the server
- A mobile phone with camera (optional, for mobile testing)

## Quick Start

```bash
# 1. Set up API key
cp .env.example .env
# Edit .env and add your Anthropic API key

# 2. Generate SSL certificate (required for camera on mobile)
./generate_cert.sh

# 3. Start the application
./run.sh
```

**For mobile access on WSL2:** See [MOBILE_ACCESS_GUIDE.md](MOBILE_ACCESS_GUIDE.md)

## Detailed Setup Instructions

### 1. Install Dependencies

The dependencies are already installed in the virtual environment. If needed:

```bash
./venv/bin/pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 3. Generate SSL Certificate (Required for Mobile)

**Important:** HTTPS is required for camera access on mobile devices.

```bash
./generate_cert.sh
```

This creates a self-signed certificate in the `certs/` directory.

### 4. Run the Application

```bash
./run.sh
```

The server will start and display:
- Local access URL: `https://localhost:5000`
- Network access URL: `https://<your-ip>:5000`

### 5. Access from Mobile

#### For WSL2 Users (Windows Subsystem for Linux)

If you're running on WSL2, you need to set up port forwarding:

**Option A - Automated Setup (Recommended):**

1. Copy `setup_windows_portforward.ps1` to your Windows desktop
2. Right-click on PowerShell and select "Run as Administrator"
3. Navigate to the file and run:
   ```powershell
   .\setup_windows_portforward.ps1
   ```
4. The script will display your Windows IP address to use on mobile

**Option B - Manual Setup:**

1. Get your WSL IP address (in WSL terminal):
   ```bash
   ./get_network_info.sh
   ```

2. Run in Windows PowerShell as Administrator:
   ```powershell
   # Replace WSL_IP with your actual WSL IP (e.g., 172.23.89.69)
   netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=WSL_IP

   # Add firewall rule
   New-NetFirewallRule -DisplayName "Waste Sorting App" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
   ```

3. Get your Windows WiFi IP address (in Windows PowerShell):
   ```powershell
   ipconfig
   ```
   Look for "Wireless LAN adapter Wi-Fi" → "IPv4 Address"

4. Access from mobile: `http://<Windows-IP>:5000`

#### For Native Linux/Mac Users

1. Make sure your mobile phone is connected to the same WiFi network as your laptop
2. On your mobile phone's browser, navigate to: `http://<your-laptop-ip>:5000`
3. Allow camera permissions when prompted

## Usage

1. **Capture Photo**: Click the "Capture Photo" button to take a picture of the waste item
2. **Analyze**: Click "Analyze Waste" to send the image to Claude for classification
3. **View Results**: See the waste category, confidence level, reasoning, and detected items
4. **Retake**: Click "Retake Photo" to capture a new image

## Waste Categories

- **Organic**: Food scraps, plant materials, biodegradable items
- **Inorganic**: Plastics, glass, metal, paper, cardboard
- **Hazardous**: Batteries, electronics, chemicals, medical waste

## Troubleshooting

### Camera not working
- Make sure you've granted camera permissions to your browser
- Try using HTTPS or localhost (some browsers restrict camera access on HTTP)
- On mobile, ensure you're using a browser that supports camera access (Chrome, Safari)

### Cannot access from mobile
- Verify both devices are on the same WiFi network
- Check if your laptop's firewall is blocking port 5000
- Try disabling the firewall temporarily for testing

### API errors
- Verify your Anthropic API key is correct in the `.env` file
- Check if you have sufficient API credits
- Ensure you have internet connection for API calls

## Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: Anthropic Claude 3.5 Sonnet (Vision)
- **Camera**: MediaDevices API

## Project Structure

```
waste-sorting-app/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .env.example          # Example env file
├── README.md             # This file
└── static/
    └── index.html        # Frontend application
```

## License

MIT
