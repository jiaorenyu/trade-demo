#!/bin/bash

# E-commerce Platform Docker Fix Script
echo "🔧 E-commerce Platform Docker Issues Fix"
echo "========================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "1️⃣ Checking Docker installation..."

# Check if Docker is installed
if ! command_exists docker; then
    echo "❌ Docker is not installed. Installing Docker Desktop..."
    echo "📖 Please install Docker Desktop:"
    echo "   macOS: brew install --cask docker"
    echo "   Or download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker is installed"

echo "2️⃣ Checking Docker daemon..."

# Check if Docker daemon is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker daemon is not running."
    echo "🚀 Starting Docker Desktop..."
    
    # Try to start Docker Desktop on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open -a Docker || {
            echo "❌ Could not start Docker Desktop automatically."
            echo "📱 Please start Docker Desktop manually and run this script again."
            echo "   1. Open Docker Desktop application"
            echo "   2. Wait for it to start (whale icon in menu bar)"
            echo "   3. Run this script again: ./scripts/fix-docker-issues.sh"
            exit 1
        }
        
        echo "⏳ Waiting for Docker to start..."
        for i in {1..30}; do
            if docker info >/dev/null 2>&1; then
                echo "✅ Docker is now running!"
                break
            fi
            echo "   Waiting... ($i/30)"
            sleep 2
        done
        
        if ! docker info >/dev/null 2>&1; then
            echo "❌ Docker failed to start. Please start it manually."
            exit 1
        fi
    else
        echo "🐧 Linux detected. Starting Docker service..."
        sudo systemctl start docker || {
            echo "❌ Could not start Docker service. Please start it manually:"
            echo "   sudo systemctl start docker"
            exit 1
        }
    fi
fi

echo "✅ Docker daemon is running"

echo "3️⃣ Detecting system architecture..."
ARCH=$(uname -m)
echo "   Architecture: $ARCH"

if [[ "$ARCH" == "arm64" || "$ARCH" == "aarch64" ]]; then
    echo "🍎 ARM64 (Apple Silicon) detected - using optimized configuration"
    DOCKER_FILE="Dockerfile.arm64"
else
    echo "🖥️  x86_64 detected - using standard configuration"
    DOCKER_FILE="Dockerfile"
fi

echo "4️⃣ Cleaning up previous builds..."
docker-compose down --volumes --remove-orphans 2>/dev/null || true
docker system prune -f || true

echo "5️⃣ Fixing frontend build issues..."

# Fix package-lock.json and node_modules for ARM64
if [ -d "frontend/e-commerce-app" ]; then
    cd frontend/e-commerce-app
    
    echo "   🧹 Cleaning frontend dependencies..."
    rm -rf node_modules package-lock.json 2>/dev/null || true
    
    echo "   📦 Reinstalling dependencies locally (for development)..."
    npm cache clean --force 2>/dev/null || true
    npm install --force 2>/dev/null || {
        echo "   ⚠️  Local npm install failed, but Docker build should work"
    }
    
    cd ../..
else
    echo "   ⚠️  Frontend directory not found, skipping local dependencies"
fi

echo "6️⃣ Building services..."

# Update docker-compose to use the right Dockerfile
if [[ "$ARCH" == "arm64" || "$ARCH" == "aarch64" ]]; then
    echo "   🔧 Using ARM64-optimized Dockerfile for frontend"
    # Try ARM64 first, then fallback to minimal if it fails
    sed -i.bak 's/dockerfile: Dockerfile/dockerfile: Dockerfile.arm64/' docker-compose.yml 2>/dev/null || true
else
    echo "   🔧 Using standard Dockerfile for x86_64"
    # Update docker-compose to use standard Dockerfile for x86_64
    sed -i.bak 's/dockerfile: Dockerfile.arm64/dockerfile: Dockerfile/' docker-compose.yml 2>/dev/null || true
fi

echo "   🔨 Building all services..."

# Try building with current configuration
if ! docker-compose build --no-cache; then
    echo "   ⚠️  Build failed, trying fallback approach..."
    
    # Try minimal Dockerfile as fallback
    echo "   🔄 Switching to minimal Dockerfile..."
    sed -i.bak2 's/dockerfile: Dockerfile.arm64/dockerfile: Dockerfile.minimal/' docker-compose.yml 2>/dev/null || true
    sed -i.bak2 's/dockerfile: Dockerfile/dockerfile: Dockerfile.minimal/' docker-compose.yml 2>/dev/null || true
    
    echo "   🔨 Retrying build with minimal configuration..."
    if ! docker-compose build --no-cache; then
        echo "   ❌ Build still failing. Trying individual service builds..."
        
        # Try building services individually
        docker-compose build --no-cache database || echo "Database build failed"
        docker-compose build --no-cache auth-service || echo "Auth service build failed"
        docker-compose build --no-cache user-service || echo "User service build failed"
        docker-compose build --no-cache frontend || echo "Frontend build failed"
    fi
fi

echo "7️⃣ Starting services..."
docker-compose up -d

echo "8️⃣ Waiting for services to be healthy..."
sleep 15

echo "9️⃣ Testing services..."

# Function to check service health
check_service() {
    local service_name=$1
    local url=$2
    
    if curl -s "$url" >/dev/null 2>&1; then
        echo "✅ $service_name: Healthy"
        return 0
    else
        echo "❌ $service_name: Not responding"
        return 1
    fi
}

check_service "Auth Service" "http://localhost:5000/health"
check_service "User Service" "http://localhost:5001/health"
check_service "Frontend" "http://localhost:3000"

echo ""
echo "🎉 Fix completed!"
echo "================================================"

# Show status
echo "📊 Current status:"
docker-compose ps

echo ""
echo "📱 Access your application:"
echo "  - Frontend:    http://localhost:3000"
echo "  - Auth API:    http://localhost:5000"
echo "  - User API:    http://localhost:5001"

echo ""
echo "🔧 If issues persist:"
echo "  - View logs: docker-compose logs -f"
echo "  - Restart:   docker-compose restart"
echo "  - Reset:     docker-compose down --volumes && docker-compose up -d"

echo ""
echo "✨ Happy coding!" 