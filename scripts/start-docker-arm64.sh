#!/bin/bash

# E-commerce Platform Docker Startup Script - ARM64 (Apple Silicon) Optimized
echo "🍎 E-commerce Platform - ARM64 (Apple Silicon) Startup"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on ARM64 (Apple Silicon)
ARCH=$(uname -m)
if [[ "$ARCH" != "arm64" ]]; then
    print_warning "This script is optimized for ARM64 (Apple Silicon). Detected: $ARCH"
    print_warning "Consider using the standard startup script instead."
fi

print_status "Architecture: $ARCH"

# Check Docker installation
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker Desktop for Mac."
    echo "Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    print_error "Docker is not running. Please start Docker Desktop."
    echo "You can start it by:"
    echo "1. Open Docker Desktop application"
    echo "2. Wait for the whale icon to appear in the menu bar"
    echo "3. Run this script again"
    exit 1
fi

print_success "Docker is running"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not available"
        exit 1
    else
        print_status "Using 'docker compose' (new syntax)"
        COMPOSE_CMD="docker compose"
    fi
else
    print_status "Using 'docker-compose' (legacy syntax)"
    COMPOSE_CMD="docker-compose"
fi

# Stop any existing containers
print_status "Stopping existing containers..."
$COMPOSE_CMD down 2>/dev/null || true

# Clean up old images and volumes (optional)
read -p "Do you want to clean up old Docker data? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Cleaning up Docker data..."
    docker system prune -f
    docker volume prune -f
fi

# Set environment variables for ARM64
export DOCKER_DEFAULT_PLATFORM=linux/arm64
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

# Build and start services
print_status "Building ARM64-optimized containers..."
if ! $COMPOSE_CMD build --no-cache; then
    print_error "Build failed. Check the logs above for details."
    exit 1
fi

print_success "Build completed successfully"

print_status "Starting services..."
if ! $COMPOSE_CMD up -d; then
    print_error "Failed to start services. Check the logs with: $COMPOSE_CMD logs"
    exit 1
fi

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."
sleep 10

# Function to check service health
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            print_success "$service_name is healthy"
            return 0
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            print_error "$service_name failed to become healthy"
            return 1
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
}

# Check service health
print_status "Checking service health..."
echo -n "Database: "
sleep 5  # Give database extra time

echo -n "Auth Service: "
check_service "Auth Service" "http://localhost:5000/health"

echo -n "User Service: "
check_service "User Service" "http://localhost:5001/health"

echo -n "Frontend: "
check_service "Frontend" "http://localhost:3000"

# Show final status
echo ""
print_success "🎉 E-commerce Platform is running!"
echo ""
echo "📱 Access your application:"
echo "  Frontend:    http://localhost:3000"
echo "  Auth API:    http://localhost:5000"
echo "  User API:    http://localhost:5001"
echo "  Database:    localhost:5432"
echo ""
echo "🔧 Useful commands:"
echo "  View logs:   $COMPOSE_CMD logs -f"
echo "  Stop all:    $COMPOSE_CMD down"
echo "  Restart:     $COMPOSE_CMD restart"
echo "  Status:      $COMPOSE_CMD ps"
echo ""
echo "💡 Optimized for ARM64 (Apple Silicon) architecture" 