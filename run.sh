#!/bin/bash
# Script to run the application locally without Docker
# This script will:
# 1. Create virtual environment if it doesn't exist
# 2. Install dependencies
# 3. Run the application

echo "Setting up local environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        echo "Creating .env file from env.example..."
        cp env.example .env
        echo "Please update .env file with your database configuration!"
    else
        echo "Creating .env file..."
        echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tododb" > .env
        echo "Please update .env file with your database configuration!"
    fi
fi

# Run the application
echo "Starting application..."
echo "API will be available at: http://localhost:8000"
echo "API docs will be available at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

