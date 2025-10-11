#!/bin/bash

# DataZen - AI Deepfake Detection Platform
# Quick Start Script

echo "=========================================="
echo "DataZen - IBM Z Datathon 2025"
echo "AI-Driven Deepfake Detection Platform"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv ../venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ../venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the Flask server
echo ""
echo "Starting Flask server..."
echo "Application will be available at: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo "=========================================="
echo ""

cd backend
python app.py

