import os
import base64
import json
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from anthropic import Anthropic, APIError, RateLimitError, APIStatusError
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
    max_retries = 3
    retry_delay = 2  # seconds

    try:
        data = request.json
        image_data = data.get('image')

        if not image_data:
            return jsonify({
                'error': 'No image provided',
                'user_message': 'Please capture a photo first.'
            }), 400

        # Remove the data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        # Retry logic for API calls
        last_error = None
        for attempt in range(max_retries):
            try:
                # Create the message with vision
                message = client.messages.create(
                    model="claude-haiku-4-5-20251001",
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

If the image does not clearly show waste, or if you cannot confidently classify it, use "UNKNOWN" as the category.

Respond in JSON format with the following structure:
{
  "category": "ORGANIC" | "INORGANIC" | "HAZARDOUS" | "UNKNOWN",
  "confidence": "high" | "medium" | "low",
  "reasoning": "Brief explanation of why this waste belongs to this category, or why it cannot be classified",
  "items_detected": ["list of items you can see"]
}

IMPORTANT: Respond with ONLY the raw JSON object. Do not wrap it in markdown code blocks or use ```json. Just return the plain JSON."""
                                }
                            ],
                        }
                    ],
                )

                # Extract the response text
                response_text = message.content[0].text

                # Clean up response text - remove markdown code blocks if present
                response_text = response_text.strip()
                if response_text.startswith('```'):
                    # Remove opening code block (```json or ```)
                    lines = response_text.split('\n')
                    if lines[0].startswith('```'):
                        lines = lines[1:]
                    # Remove closing code block (```)
                    if lines and lines[-1].strip() == '```':
                        lines = lines[:-1]
                    response_text = '\n'.join(lines).strip()

                # Parse the JSON response from Claude
                result = json.loads(response_text)

                # Validate the response structure
                required_fields = ['category', 'confidence', 'reasoning', 'items_detected']
                if not all(field in result for field in required_fields):
                    raise ValueError("Invalid response format from AI")

                # Validate category
                valid_categories = ['ORGANIC', 'INORGANIC', 'HAZARDOUS', 'UNKNOWN']
                if result['category'] not in valid_categories:
                    result['category'] = 'UNKNOWN'
                    result['reasoning'] = f"Could not classify as one of the three main categories. Original classification: {result.get('category', 'N/A')}"

                return jsonify(result)

            except APIStatusError as e:
                last_error = e
                error_code = e.status_code

                # Handle specific API errors
                if error_code == 529:  # Overloaded
                    if attempt < max_retries - 1:
                        print(f"API overloaded, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        return jsonify({
                            'error': 'api_overloaded',
                            'user_message': 'The AI service is currently overloaded. Please try again in a few moments.'
                        }), 503

                elif error_code == 429:  # Rate limit
                    return jsonify({
                        'error': 'rate_limit',
                        'user_message': 'Too many requests. Please wait a moment before trying again.'
                    }), 429

                elif error_code == 401:  # Authentication error
                    return jsonify({
                        'error': 'authentication_error',
                        'user_message': 'API key is invalid. Please check the server configuration.'
                    }), 500

                else:
                    return jsonify({
                        'error': 'api_error',
                        'user_message': f'An API error occurred: {str(e)}'
                    }), 500

            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print(f"Response text: {response_text}")
                return jsonify({
                    'error': 'json_parse_error',
                    'user_message': 'Could not understand the AI response. Please try again.'
                }), 500

            except ValueError as e:
                print(f"Validation error: {str(e)}")
                return jsonify({
                    'error': 'validation_error',
                    'user_message': 'The AI response was incomplete. Please try again.'
                }), 500

        # If we exhausted all retries
        if last_error:
            return jsonify({
                'error': 'max_retries_exceeded',
                'user_message': 'Could not process the image after multiple attempts. Please try again later.'
            }), 503

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'unexpected_error',
            'user_message': 'An unexpected error occurred. Please try again.'
        }), 500

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))

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
    print(f"Access from this computer: {protocol}://localhost:{port}")
    print(f"Access from mobile phone: {protocol}://{local_ip}:{port}")

    if use_ssl:
        print(f"\n⚠️  NOTE: You will see a security warning because of the")
        print(f"   self-signed certificate. Click 'Advanced' and proceed.")
    else:
        print(f"\n⚠️  WARNING: Running without SSL!")
        print(f"   Camera may not work on mobile. Run ./generate_cert.sh")

    print(f"{'='*60}\n")

    # Run on all network interfaces so it's accessible on local network
    if use_ssl:
        app.run(host='0.0.0.0', port=port, debug=True,
                ssl_context=(cert_file, key_file))
    else:
        app.run(host='0.0.0.0', port=port, debug=True)
