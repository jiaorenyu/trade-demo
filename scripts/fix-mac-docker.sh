#!/bin/bash

# macOS Docker Fix Script - Resolves common ARM64/Docker issues
echo "🍎 macOS Docker Fix Script"
echo "========================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

print_status "Checking system..."
echo "Architecture: $(uname -m)"
echo "macOS Version: $(sw_vers -productVersion)"

# Step 1: Check Docker Desktop
print_status "Checking Docker Desktop..."
if ! command -v docker &> /dev/null; then
    print_error "Docker Desktop not found!"
    echo "Please install Docker Desktop for Mac:"
    echo "1. Download from: https://www.docker.com/products/docker-desktop"
    echo "2. Install and start Docker Desktop"
    echo "3. Wait for the whale icon in menu bar"
    echo "4. Run this script again"
    exit 1
fi

# Step 2: Start Docker if not running
if ! docker info &> /dev/null; then
    print_warning "Docker is not running. Attempting to start..."
    
    # Try to start Docker Desktop
    open -a Docker 2>/dev/null || {
        print_error "Could not start Docker Desktop automatically"
        echo "Please manually:"
        echo "1. Open Docker Desktop application"
        echo "2. Wait for it to start (whale icon in menu bar)"
        echo "3. Run this script again"
        exit 1
    }
    
    print_status "Waiting for Docker to start..."
    for i in {1..60}; do
        if docker info &> /dev/null; then
            print_success "Docker is now running!"
            break
        fi
        if [ $i -eq 60 ]; then
            print_error "Docker failed to start within 60 seconds"
            echo "Please start Docker Desktop manually and try again"
            exit 1
        fi
        echo -n "."
        sleep 1
    done
fi

print_success "Docker is running"

# Step 3: Fix proxy conflicts
print_status "Resolving proxy conflicts..."
docker-compose down --remove-orphans 2>/dev/null || true
docker container stop $(docker container ls -aq) 2>/dev/null || true
docker container rm $(docker container ls -aq) 2>/dev/null || true
docker network prune -f 2>/dev/null || true
docker system prune -f 2>/dev/null || true

# Step 4: Fix port conflicts
print_status "Checking for port conflicts..."
for port in 3000 5000 5001 5432; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $port is in use"
        echo "Processes using port $port:"
        lsof -Pi :$port -sTCP:LISTEN
        echo ""
        read -p "Kill processes on port $port? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            lsof -ti:$port | xargs kill -9 2>/dev/null || true
            print_success "Cleared port $port"
        fi
    fi
done

# Step 5: Set ARM64 environment
print_status "Setting ARM64 environment..."
export DOCKER_DEFAULT_PLATFORM=linux/arm64
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

# Step 6: Clean build
print_status "Building ARM64 containers..."
docker-compose build --no-cache --pull

if [ $? -ne 0 ]; then
    print_error "Build failed. Common solutions:"
    echo "1. Restart Docker Desktop completely"
    echo "2. Increase Docker memory to 4GB+ in settings"
    echo "3. Check internet connection"
    echo "4. Try: docker system prune -a --volumes"
    exit 1
fi

print_success "Build completed"

# Step 7: Start services
print_status "Starting services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    print_error "Startup failed. Checking logs..."
    docker-compose logs
    exit 1
fi

# Step 8: Health checks
print_status "Waiting for services..."
sleep 15

# Check each service
services_ok=true

check_service() {
    local name=$1
    local url=$2
    local attempts=10
    
    for i in $(seq 1 $attempts); do
        if curl -s "$url" >/dev/null 2>&1; then
            print_success "$name is healthy"
            return 0
        fi
        sleep 2
    done
    
    print_error "$name failed health check"
    return 1
}

check_service "Frontend" "http://localhost:3000" || services_ok=false
check_service "Auth Service" "http://localhost:5000/health" || services_ok=false
check_service "User Service" "http://localhost:5001/health" || services_ok=false

if [ "$services_ok" = true ]; then
    echo ""
    print_success "🎉 All services are running!"
    echo ""
    echo "📱 Access your application:"
    echo "  Frontend:    http://localhost:3000"
    echo "  Auth API:    http://localhost:5000/health"
    echo "  User API:    http://localhost:5001/health"
    echo ""
    echo "🔧 Useful commands:"
    echo "  View logs:   docker-compose logs -f"
    echo "  Stop all:    docker-compose down"
    echo "  Restart:     docker-compose restart"
    echo "  Status:      docker-compose ps"
else
    print_warning "Some services may not be fully ready yet"
    echo "Check individual service logs: docker-compose logs [service-name]"
fi

echo ""
print_success "macOS Docker fix completed!" 