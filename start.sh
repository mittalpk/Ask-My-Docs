#!/bin/bash
# AskMyDocs Quick Start Script

echo "🚀 Starting AskMyDocs..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker and Docker Compose first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Create environment files if they don't exist
if [ ! -f "askmydocs-backend/.env" ]; then
    echo "📝 Creating backend .env file..."
    cp askmydocs-backend/.env.example askmydocs-backend/.env
fi

if [ ! -f "askmydocs-frontend/.env" ]; then
    echo "📝 Creating frontend .env file..."
    cp askmydocs-frontend/.env.example askmydocs-frontend/.env
fi

echo "🐳 Starting Docker containers..."
docker-compose up --build

echo ""
echo "✅ AskMyDocs is starting up!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000/docs"
echo ""
echo "📖 First time setup may take 2-3 minutes to download AI models."
echo "💡 Create an account and start uploading documents!"