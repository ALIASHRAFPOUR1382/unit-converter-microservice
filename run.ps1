# Script to run the application locally without Docker
# This script will:
# 1. Create virtual environment if it doesn't exist
# 2. Install dependencies
# 3. Run the application

Write-Host "Setting up local environment..." -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install/upgrade dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Check if .env file exists
if (-not (Test-Path ".env")) {
    if (Test-Path "env.example") {
        Write-Host "Creating .env file from env.example..." -ForegroundColor Yellow
        Copy-Item env.example .env
        Write-Host "Please update .env file with your database configuration!" -ForegroundColor Yellow
    } else {
        Write-Host "Creating .env file..." -ForegroundColor Yellow
        @"
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tododb
"@ | Out-File -FilePath .env -Encoding utf8
        Write-Host "Please update .env file with your database configuration!" -ForegroundColor Yellow
    }
}

# Run the application
Write-Host "Starting application..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API docs will be available at: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

