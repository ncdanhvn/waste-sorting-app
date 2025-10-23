#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create a .env file with your Anthropic API key."
    echo ""
    echo "Steps:"
    echo "1. Copy the example file: cp .env.example .env"
    echo "2. Edit .env and add your API key"
    echo "3. Run this script again"
    exit 1
fi

# Check if API key is set
if grep -q "your_api_key_here" .env; then
    echo "ERROR: Please set your actual Anthropic API key in .env file"
    exit 1
fi

# Activate virtual environment and run
source venv/bin/activate
python app.py
