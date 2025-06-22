#!/bin/bash

# E-commerce Platform Docker Startup Script
echo "🚀 Starting E-commerce Platform with Docker"
echo "============================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed
if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "📖 Install guide:"
    echo "   macOS: brew install --cask docker"
    echo "   Linux: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker daemon is not running. Please start Docker Desktop or the Docker service."
    exit 1
fi

# Check if Docker Compose is available
if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    echo "   Usually included with Docker Desktop."
    exit 1
fi

# Stop and remove existing containers (optional cleanup)
echo "🧹 Cleaning up existing containers..."
if docker compose version >/dev/null 2>&1; then
    docker compose down --volumes --remove-orphans 2>/dev/null || true
else
    docker-compose down --volumes --remove-orphans 2>/dev/null || true
fi

# Build and start services
echo "🔨 Building and starting services..."
echo "This may take a few minutes on first run..."

if docker compose version >/dev/null 2>&1; then
    docker compose up --build -d
else
    docker-compose up --build -d
fi

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
echo "Checking database startup..."
sleep 10

# Check if services are starting
echo "🔍 Checking service health..."
sleep 10

# Function to check service health
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            echo "✅ $service_name: Healthy"
            return 0
        fi
        sleep 2
        ((attempt++))
    done
    echo "❌ $service_name: Not responding after ${max_attempts} attempts"
    return 1
}

# Check database (just try to connect via docker)
DB_STATUS=$(docker ps --filter "name=database" --format "{{.Status}}" 2>/dev/null)
if [[ $DB_STATUS == *"Up"* ]]; then
    echo "✅ Database: Running"
else
    echo "❌ Database: Not running"
fi

# Check services
check_service "Auth Service" "http://localhost:5000/health"
check_service "User Service" "http://localhost:5001/health"
check_service "Frontend" "http://localhost:3000"

echo ""
echo "🎉 E-commerce Platform is ready!"
echo "================================================"
echo "📱 Access your application:"
echo "  - Frontend:    http://localhost:3000"
echo "  - Auth API:    http://localhost:5000"
echo "  - User API:    http://localhost:5001"
echo "  - Database:    localhost:5432"
echo ""
echo "🧪 Test your setup:"
echo "  curl http://localhost:5000/health"
echo "  curl http://localhost:5001/health"
echo "  python test_services.py"
echo ""
echo "📝 Useful Docker commands:"
echo "  - View logs:      docker-compose logs -f"
echo "  - Stop services:  docker-compose down"
echo "  - Restart:        docker-compose restart"
echo "  - View status:    docker-compose ps"
echo ""
echo "🔧 Development workflow:"
echo "  1. Make code changes"
echo "  2. docker-compose up --build -d"
echo "  3. Test your changes"
echo ""
echo "✨ Happy coding!" 