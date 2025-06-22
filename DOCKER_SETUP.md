# 🐳 Docker Setup Guide

This guide will help you run your e-commerce platform using Docker containers.

## 🚀 Quick Start

```bash
# Using the automated script (recommended)
./scripts/start-docker.sh

# OR manually
docker-compose up --build -d
```

## 📋 Prerequisites

### Docker Installation

#### macOS
```bash
# Install Docker Desktop
brew install --cask docker

# Verify installation
docker --version
docker-compose --version
```

#### Linux (Ubuntu/Debian)
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Add user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

#### Windows
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Ensure WSL2 is enabled for better performance

## 🏗️ Architecture

The containerized setup includes:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Auth Service   │    │  User Service   │
│   (React)       │    │   (Flask)       │    │   (Flask)       │
│   Port: 3000    │    │   Port: 5000    │    │   Port: 5001    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   Database      │
                    │   Port: 5432    │
                    └─────────────────┘
```

## 🔧 Configuration

### Environment Variables

The containers use these environment variables:

#### Database Service
- `POSTGRES_DB`: ecommerce_db
- `POSTGRES_USER`: ecommerce_user  
- `POSTGRES_PASSWORD`: ecommerce_pass

#### Backend Services
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret for JWT token signing
- `FLASK_ENV`: development/production

#### Frontend Service
- `VITE_API_BASE_URL`: Backend API URL
- `VITE_USER_SERVICE_URL`: User service URL

### Custom Configuration

Create `.env` files to override defaults:

```bash
# .env (for Docker)
JWT_SECRET_KEY=your-super-secure-secret-key
DATABASE_PASSWORD=your-secure-password
FLASK_ENV=production
```

## 🚀 Running Services

### Basic Commands

```bash
# Start all services
docker-compose up -d

# Start with build (after code changes)
docker-compose up --build -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f auth-service

# Stop services
docker-compose down

# Stop and remove volumes (complete cleanup)
docker-compose down --volumes

# Restart specific service
docker-compose restart auth-service

# Shell into container
docker-compose exec auth-service /bin/bash
```

## 🔍 Testing Containerized Services

### Health Checks

All services include health checks:

```bash
# Check all service health
curl http://localhost:5000/health  # Auth Service
curl http://localhost:5001/health  # User Service
curl http://localhost:3000         # Frontend

# Using Docker Compose
docker-compose ps
```

### API Testing

```bash
# Register a user
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Test with token (replace with actual token)
TOKEN="your-jwt-token-here"
curl -X GET http://localhost:5001/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Integration Test

```bash
# Run the integration test script
python test_services.py
```

## 🛠️ Development Workflow

### Making Code Changes

1. **Stop containers:**
   ```bash
   docker-compose down
   ```

2. **Make your changes** to the source code

3. **Rebuild and restart:**
   ```bash
   docker-compose up --build -d
   ```

### Database Changes

If you modify the database schema:

```bash
# Stop services and remove volumes
docker-compose down --volumes

# Start fresh (will reinitialize DB)
docker-compose up --build -d
```

### Hot Reloading (Development)

For faster development, you can mount source code:

```yaml
# In docker-compose.override.yml
version: '3.8'
services:
  auth-service:
    volumes:
      - ./backend/auth-service:/app
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: 1
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different ports in compose file
```

#### 2. Docker Daemon Not Running
```bash
# Start Docker Desktop (macOS/Windows)
# Or start Docker service (Linux)
sudo systemctl start docker

# Check Docker status
docker info
```

#### 3. Build Failures
```bash
# Clean Docker build cache
docker builder prune -a

# Force rebuild
docker-compose build --no-cache

# Check available disk space
docker system df
```

#### 4. Database Connection Issues
```bash
# Check if database container is running
docker-compose ps database

# View database logs
docker-compose logs database

# Connect to database directly
docker-compose exec database psql -U ecommerce_user -d ecommerce_db
```

#### 5. Service Health Check Failures
```bash
# Wait longer for services to start
sleep 30

# Check container logs
docker-compose logs auth-service

# Manual health check
docker-compose exec auth-service curl localhost:5000/health
```

### Debugging

#### Container Shell Access
```bash
# Access running container
docker-compose exec auth-service /bin/bash

# If container is not running, run a temporary one
docker run -it --rm ecommerce-auth-service /bin/bash
```

#### View Container Resources
```bash
# Resource usage
docker stats

# Container processes
docker-compose top
```

#### Network Debugging
```bash
# List networks
docker network ls

# Inspect network
docker network inspect trade-demo_ecommerce-network
```

## 🔒 Security Considerations

### Development
- ✅ Non-root users in containers
- ✅ Health checks enabled
- ✅ Secrets via environment variables
- ⚠️ Default passwords (change in production)

### Production
- 🔐 Use Docker secrets management
- 🔐 Enable TLS/SSL
- 🔐 Use trusted base images
- 🔐 Regular security updates
- 🔐 Network policies
- 🔐 Non-default passwords

## 📊 Monitoring

### Container Monitoring
```bash
# Resource usage
docker stats

# Container processes
docker-compose top

# System information
docker system df
```

### Application Monitoring
```bash
# Service logs
docker-compose logs -f --tail=100 auth-service

# Health status monitoring
while true; do
  curl -s http://localhost:5000/health || echo "Service down"
  sleep 5
done
```

## 🚀 Production Deployment

### Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml ecommerce

# Scale services
docker service scale ecommerce_auth-service=3
```

### Kubernetes
```bash
# Convert compose to Kubernetes manifests
kompose convert -f docker-compose.yml

# Deploy to Kubernetes
kubectl apply -f .
```

### Cloud Deployment
- **AWS**: ECS, EKS, or Fargate
- **GCP**: Cloud Run, GKE
- **Azure**: Container Instances, AKS

## 📋 Checklist

### Before First Run
- [ ] Docker installed and running
- [ ] Docker Compose available
- [ ] Ports 3000, 5000, 5001, 5432 available
- [ ] Script is executable (`chmod +x scripts/start-docker.sh`)

### Development Checklist
- [ ] Code changes made
- [ ] Containers rebuilt (`--build` flag)
- [ ] Health checks passing
- [ ] Integration tests pass
- [ ] Documentation updated

### Production Checklist
- [ ] Secure passwords set
- [ ] TLS certificates configured
- [ ] Monitoring setup
- [ ] Backup strategy
- [ ] CI/CD pipeline
- [ ] Security scanning

---

## 🎯 Next Steps

1. **Scale Services**: Add more instances of each service
2. **Add API Gateway**: Implement Nginx reverse proxy
3. **Implement Caching**: Add Redis for session storage
4. **Add Monitoring**: Implement Prometheus + Grafana
5. **Security Hardening**: Add authentication, rate limiting
6. **CI/CD Pipeline**: Automate builds and deployments

**Happy Containerizing! 🐳** 