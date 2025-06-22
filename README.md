# 🍎 E-commerce Platform - ARM64 (Apple Silicon) Guide

## Quick Start for macOS with Apple Silicon

### Prerequisites
- **macOS** with Apple Silicon (M1, M2, M3 chips)
- **Docker Desktop for Mac** (latest version)
- **Git**

### 🚀 One-Command Startup

```bash
./scripts/start-docker-arm64.sh
```

This script will:
- ✅ Detect ARM64 architecture
- ✅ Check Docker installation and status
- ✅ Build ARM64-optimized containers
- ✅ Start all services
- ✅ Verify health checks
- ✅ Display access URLs

### 📱 Access Your Application

Once started, you can access:
- **Frontend**: http://localhost:3000
- **Auth API**: http://localhost:5000/health
- **User API**: http://localhost:5001/health
- **Database**: localhost:5432

### 🔧 Manual Commands

If you prefer manual control:

```bash
# Set ARM64 environment
export DOCKER_DEFAULT_PLATFORM=linux/arm64
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

# Build and start
docker-compose build --no-cache
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### 🏗️ ARM64 Optimizations

Our setup includes these Apple Silicon optimizations:

#### **Dockerfiles**
- Platform specification: `--platform=linux/arm64`
- ARM64-compatible base images
- Optimized dependency installation
- Proper build tool chains for ARM64

#### **Frontend (React/Vite)**
- Node.js ARM64 optimizations
- Increased memory allocation: `NODE_OPTIONS="--max-old-space-size=4096"`
- Proper Rollup/Vite configuration for ARM64
- Build dependencies for native modules

#### **Backend (Python/Flask)**
- Python 3.11 Alpine ARM64
- Individual package installation to avoid conflicts
- Simplified auth service (no email dependencies)
- PostgreSQL ARM64 drivers

#### **Database (PostgreSQL)**
- PostgreSQL 17 Alpine ARM64
- Proper encoding settings for ARM64
- Optimized initialization scripts

### 🛠️ Troubleshooting

#### **Docker Issues**
```bash
# Restart Docker Desktop
# Quit Docker Desktop completely, then restart

# Clean Docker data
docker system prune -a --volumes
docker volume prune -f

# Rebuild everything
./scripts/start-docker-arm64.sh
```

#### **Build Failures**
```bash
# Check architecture
uname -m  # Should show 'arm64'

# Force ARM64 build
export DOCKER_DEFAULT_PLATFORM=linux/arm64
docker-compose build --no-cache --pull
```

#### **Port Conflicts**
```bash
# Check what's using ports
lsof -i :3000
lsof -i :5000
lsof -i :5001

# Kill conflicting processes
sudo lsof -ti:3000 | xargs kill -9
```

#### **Memory Issues**
```bash
# Increase Docker memory allocation in Docker Desktop settings
# Recommended: 4GB+ for ARM64 builds
```

### 📊 Service Health Checks

All services include health checks optimized for ARM64:

```bash
# Check individual services
curl http://localhost:5000/health  # Auth Service
curl http://localhost:5001/health  # User Service  
curl http://localhost:3000         # Frontend

# View container status
docker-compose ps
```

### 🔍 Development Tips

#### **Local Development**
```bash
# For local development without Docker
cd backend/auth-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app_simple.py

# Frontend development
cd frontend/e-commerce-app
npm install
npm run dev
```

#### **Database Access**
```bash
# Connect to PostgreSQL
psql -h localhost -p 5432 -U ecommerce_user -d ecommerce_db

# View database in container
docker-compose exec database psql -U ecommerce_user -d ecommerce_db
```

### 🚨 Known Issues & Solutions

#### **Rollup ARM64 Issues**
- **Solution**: Use our ARM64-optimized Dockerfile with proper Node.js configuration

#### **Python Email Module Conflicts**
- **Solution**: Use simplified auth service without email dependencies

#### **Port Binding Issues**
- **Solution**: Ensure no other services are using ports 3000, 5000, 5001, 5432

#### **Build Time**
- **Expected**: ARM64 builds may take 5-10 minutes on first run
- **Tip**: Use `--no-cache` flag for clean builds

### 🎯 Performance

Optimized for Apple Silicon:
- **Build Time**: ~5-10 minutes (first build)
- **Startup Time**: ~30-60 seconds
- **Memory Usage**: ~2-3GB total
- **CPU Usage**: Efficient ARM64 native execution

### 📞 Support

If you encounter issues:

1. **Check logs**: `docker-compose logs -f [service-name]`
2. **Verify architecture**: `uname -m` should show `arm64`
3. **Update Docker**: Ensure latest Docker Desktop for Mac
4. **Clean restart**: Run `./scripts/start-docker-arm64.sh` with cleanup

---

**🎉 Enjoy your ARM64-optimized e-commerce platform!** 