import os
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/classify', methods=['POST'])
def classify_waste():
    try:
        data = request.json
        image_data = data.get('image')

        if not image_data:
            return jsonify({'error': 'No image provided'}), 400

        # Remove the data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        # Create the message with vision
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze this image of waste and classify it into one of these three categories:

1. ORGANIC - Food waste, plant matter, biodegradable materials
2. INORGANIC - Plastic, glass, metal, paper, cardboard
3. HAZARDOUS - Batteries, electronics, chemicals, medical waste, light bulbs

Respond in JSON format with the following structure:
{
  "category": "ORGANIC" | "INORGANIC" | "HAZARDOUS",
  "confidence": "high" | "medium" | "low",
  "reasoning": "Brief explanation of why this waste belongs to this category",
  "items_detected": ["list of items you can see"]
}

Only respond with the JSON object, no additional text."""
                        }
                    ],
                }
            ],
        )

        # Extract the response text
        response_text = message.content[0].text

        # Parse the JSON response from Claude
        import json
        result = json.loads(response_text)

        return jsonify(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get the local IP address
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # Check if SSL certificate exists
    cert_file = 'certs/cert.pem'
    key_file = 'certs/key.pem'
    use_ssl = os.path.exists(cert_file) and os.path.exists(key_file)

    protocol = "https" if use_ssl else "http"

    print(f"\n{'='*60}")
    print(f"Waste Sorting Application is running!")
    print(f"{'='*60}")
    print(f"Access from this computer: {protocol}://localhost:5000")
    print(f"Access from mobile phone: {protocol}://{local_ip}:5000")

    if use_ssl:
        print(f"\n⚠️  NOTE: You will see a security warning because of the")
        print(f"   self-signed certificate. Click 'Advanced' and proceed.")
    else:
        print(f"\n⚠️  WARNING: Running without SSL!")
        print(f"   Camera may not work on mobile. Run ./generate_cert.sh")

    print(f"{'='*60}\n")

    # Run on all network interfaces so it's accessible on local network
    if use_ssl:
        app.run(host='0.0.0.0', port=5000, debug=True,
                ssl_context=(cert_file, key_file))
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
