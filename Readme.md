# 🛒 E-commerce Platform - Local Development Guide

A modern, scalable e-commerce platform built with microservices architecture. This guide will help you run the system on your local machine.

## 🚀 Quick Start (Recommended)

### Option 1: Containerized Setup (Docker)
```bash
# Using Docker (recommended)
./scripts/start-docker.sh

# Or manually
docker-compose up --build -d
```

**⚠️ Having Docker issues?** Choose your fix:
```bash
# Option 1: Super quick fix (starts Docker + fixes everything)
./scripts/quick-fix.sh

# Option 2: Manual approach
# 1. Start Docker Desktop manually
# 2. Run the fix script
./scripts/fix-docker-issues.sh
```

### Option 2: Manual Local Setup
See [Manual Setup](#-manual-local-setup) section below.

## 📋 Prerequisites

### For Containerized Setup (Recommended)
- **Docker Desktop** (Mac/Windows) or **Docker Engine** (Linux)
- **Docker Compose** (usually included with Docker Desktop)

### For Manual Setup
- **Python 3.13+**
- **Node.js 18+** and **npm**
- **PostgreSQL 17+**

## 🏗️ System Architecture

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

## 🐳 Docker Setup (Recommended)

### Prerequisites Installation

#### Install Docker (macOS)
```bash
# Install Docker Desktop
brew install --cask docker

# Verify installation
docker --version
docker-compose --version
```

#### Install Docker (Linux)
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

### Running with Docker

```bash
# Method 1: Automated script (recommended)
./scripts/start-docker.sh

# Method 2: Manual commands
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Management Commands

```bash
# View running containers
docker ps

# Restart specific service
docker-compose restart auth-service

# Access container shell
docker exec -it <container-name> /bin/bash

# View container logs
docker logs <container-name>

# Rebuild after code changes
docker-compose up --build -d

# Stop and remove volumes (complete cleanup)
docker-compose down --volumes
```

## 🔧 Manual Local Setup

### 1. Database Setup

```bash
# Start PostgreSQL (if not running)
brew services start postgresql@17

# Create database and user
psql postgres -c "CREATE DATABASE ecommerce_db;"
psql postgres -c "CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_pass';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;"

# Initialize database schema
psql ecommerce_db < database/init.sql

# Grant schema permissions
psql ecommerce_db -c "GRANT ALL ON SCHEMA auth_service TO ecommerce_user;"
psql ecommerce_db -c "GRANT ALL ON SCHEMA user_service TO ecommerce_user;"
psql ecommerce_db -c "GRANT ALL ON ALL TABLES IN SCHEMA auth_service TO ecommerce_user;"
psql ecommerce_db -c "GRANT ALL ON ALL TABLES IN SCHEMA user_service TO ecommerce_user;"
```

### 2. Backend Services Setup

#### Authentication Service (Terminal 1)
```bash
cd backend/auth-service

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install Flask==3.1.1 Flask-RESTful==0.3.10 Flask-JWT-Extended==4.7.1
pip install marshmallow==4.0.0 SQLAlchemy==2.0.41 werkzeug==3.1.3
pip install requests==2.31.0 python-dotenv==1.1.0
pip install email-validator psycopg2-binary

# Start service
python app_simple.py
```

#### User Service (Terminal 2)
```bash
cd backend/user-service

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start service
python app.py
```

### 3. Frontend Setup (Terminal 3)

```bash
cd frontend/e-commerce-app

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔍 Testing Your Setup

### Health Checks
```bash
# Test all services
curl http://localhost:5000/health  # Auth Service
curl http://localhost:5001/health  # User Service
curl http://localhost:3000         # Frontend

# Expected responses:
# Auth: {"status": "healthy", "service": "auth-service-simplified", "version": "1.0.0"}
# User: {"status": "healthy", "service": "user-service", "version": "1.0.0"}
# Frontend: HTML page or React app
```

### API Testing
```bash
# 1. Register a new user
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Expected: {"message": "User registered successfully", "user_id": "..."}

# 2. Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Expected: {"access_token": "...", "user": {"id": "...", "email": "..."}}

# 3. Test User Service (replace TOKEN with actual token from login)
TOKEN="your-jwt-token-here"
curl -X GET http://localhost:5001/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Integration Test
```bash
# Run the automated integration test
python test_services.py
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Permission Denied: python
```bash
# Issue: zsh: permission denied: python
# Solution: Use python3 explicitly or fix PATH
python3 app.py
# OR
export PATH="/usr/local/bin:$PATH"
```

#### 2. npm package.json not found
```bash
# Issue: npm error ENOENT: no such file or directory, open '.../package.json'
# Solution: Make sure you're in the correct directory
cd frontend/e-commerce-app
npm run dev
```

#### 3. Database Connection Failed
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# If not running, start it
brew services start postgresql@17

# Check if database exists
psql -l | grep ecommerce_db

# Check if user exists
psql postgres -c "\du" | grep ecommerce_user
```

#### 4. Port Already in Use
```bash
# Find process using the port
lsof -i :5000
lsof -i :5001
lsof -i :3000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>
```

#### 5. Module Not Found Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# For specific missing modules
pip install email-validator psycopg2-binary
```

#### 6. JWT Token Mismatch
Make sure both auth-service and user-service use the same JWT secret:
```bash
# Create .env files with same secret
echo "JWT_SECRET_KEY=your-secret-key" > backend/auth-service/.env
echo "JWT_SECRET_KEY=your-secret-key" > backend/user-service/.env
```

#### 7. Docker Build Failures
```bash
# Clear cache and rebuild
docker system prune -a
docker build --no-cache -t ecommerce-auth-service backend/auth-service/

# Check Docker daemon is running
docker info
```

#### 8. Docker Compose Issues
```bash
# Check Docker Compose version
docker-compose --version

# If using newer Docker, try:
docker compose up --build -d

# Reset everything
docker-compose down --volumes --remove-orphans
docker-compose up --build -d
```

#### 9. ARM64 (Apple Silicon) Rollup Issues
```bash
# If you see "Cannot find module @rollup/rollup-linux-arm64-musl" error:

# Option 1: Use the automated fix script (recommended)
./scripts/fix-docker-issues.sh

# Option 2: Manual fix
docker-compose down --volumes
cd frontend/e-commerce-app
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --force
cd ../..
docker-compose build --no-cache frontend
docker-compose up -d
```

## 📁 Project Structure

```
trade-demo/
├── backend/                    # Backend microservices
│   ├── auth-service/          # ✅ Authentication & JWT
│   │   ├── app.py            # Full production version
│   │   ├── app_simple.py     # Simplified version (recommended for local)
│   │   ├── Dockerfile        # Container configuration
│   │   └── requirements.txt  # Python dependencies
│   └── user-service/         # ✅ User profiles & addresses
│       ├── app.py           # User service application
│       ├── Dockerfile       # Container configuration
│       └── requirements.txt # Python dependencies
├── frontend/
│   └── e-commerce-app/       # ✅ React application
│       ├── src/             # React source code
│       ├── package.json     # Node.js dependencies
│       └── Dockerfile       # Container configuration
├── database/
│   └── init.sql             # ✅ Database schema
├── scripts/
│   └── start-docker.sh      # Docker startup script
├── docker-compose.yml       # Docker orchestration (main file)
├── test_services.py         # Integration tests
└── DOCKER_SETUP.md          # Container setup guide
```

## 🌐 Service URLs

When running locally, access your services at:

- **Frontend**: http://localhost:3000
- **Auth Service**: http://localhost:5000
- **User Service**: http://localhost:5001
- **Database**: localhost:5432

## 🔄 Development Workflow

### Making Code Changes

#### For Docker Setup (Recommended):
```bash
# 1. Stop containers
docker-compose down

# 2. Make your changes to source code

# 3. Rebuild and restart
docker-compose up --build -d
```

#### For Manual Setup:
```bash
# 1. Stop the relevant service (Ctrl+C in terminal)
# 2. Make your changes
# 3. Restart the service
python app.py  # or app_simple.py
```

### Database Changes
```bash
# Stop all services
# Update database/init.sql
# For Docker: restart with --volumes flag
docker-compose down --volumes
docker-compose up --build -d

# For manual: re-run init script
psql ecommerce_db < database/init.sql
```

## 🚀 Production Deployment

For production deployment guides, see:
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Complete containerization guide
- Cloud deployment options (AWS, GCP, Azure)
- Kubernetes deployment manifests

## 📊 Monitoring and Logs

### View Logs
```bash
# Docker logs
docker-compose logs -f auth-service
docker-compose logs -f user-service

# Manual setup logs
tail -f backend/auth-service/auth_service.log
tail -f backend/user-service/user_service.log
```

### Performance Monitoring
```bash
# Docker resource usage
docker stats

# System resource usage
top
htop
```

## 🔐 Security Notes

### Development Security
- Default passwords are used for development
- JWT secrets are hardcoded
- CORS is configured for local development

### Production Security
- Change all default passwords
- Use environment variables for secrets
- Enable HTTPS/TLS
- Configure proper CORS policies
- Use secure database connections

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** first (see Monitoring section)
2. **Verify all services are running** (health checks)
3. **Check the troubleshooting section** above
4. **Ensure dependencies are installed** correctly
5. **Try the Docker approach** if manual setup fails

## 📈 Next Steps

- ✅ **Phase 1 Complete**: Auth Service, User Service, Database
- 🔄 **Phase 2**: Product Service, Localization Service
- 📋 **Phase 3**: Order Service, Payment Service
- 🚀 **Phase 4**: API Gateway, Advanced Features

---

**Happy Coding! 🎉**

For more detailed information, see:
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Complete containerization guide
- [docs/](docs/) - Additional documentation
