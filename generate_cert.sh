#!/bin/bash

echo "Generating self-signed SSL certificate..."
echo ""

# Create certs directory if it doesn't exist
mkdir -p certs

# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes \
  -out certs/cert.pem \
  -keyout certs/key.pem \
  -days 365 \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:$(hostname -I | awk '{print $1}')"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ SSL certificate generated successfully!"
    echo "  Certificate: certs/cert.pem"
    echo "  Private Key: certs/key.pem"
    echo ""
    echo "Note: You will need to accept the security warning in your browser"
    echo "      since this is a self-signed certificate."
else
    echo ""
    echo "✗ Failed to generate certificate"
    exit 1
fi
