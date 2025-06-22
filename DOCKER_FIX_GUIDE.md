# 🔧 Docker Issues Fix Guide

## Problem: ARM64 Rollup Build Failures

### Error Message
```
Error: Cannot find module @rollup/rollup-linux-arm64-musl. npm has a bug related to optional dependencies
```

### Root Cause
- **Issue**: npm has a known bug with optional dependencies on ARM64 (Apple Silicon) architecture
- **Affected**: Frontend build process using Vite/Rollup on macOS with Apple Silicon chips
- **Impact**: Docker build fails when building the React frontend container

## 🚀 Solution: Automated Fix

### Quick Fix (Recommended)
```bash
./scripts/fix-docker-issues.sh
```

This script automatically:
1. ✅ Checks Docker installation and starts Docker Desktop if needed
2. ✅ Detects your system architecture (ARM64 vs x86_64)
3. ✅ Uses the appropriate Dockerfile for your architecture
4. ✅ Cleans npm cache and dependencies
5. ✅ Rebuilds containers with ARM64 optimizations
6. ✅ Tests all services

### Manual Fix
If you prefer to fix manually:

```bash
# 1. Start Docker Desktop manually
open -a Docker

# 2. Clean everything
docker-compose down --volumes
docker system prune -f

# 3. Fix frontend dependencies
cd frontend/e-commerce-app
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --force
cd ../..

# 4. Rebuild with ARM64-optimized Dockerfile
docker-compose build --no-cache
docker-compose up -d
```

## 📁 Files Created/Modified

### New Files
- `frontend/e-commerce-app/Dockerfile.arm64` - ARM64-optimized Dockerfile
- `frontend/e-commerce-app/.dockerignore` - Excludes unnecessary files
- `scripts/fix-docker-issues.sh` - Automated fix script
- `DOCKER_FIX_GUIDE.md` - This guide

### Modified Files
- `docker-compose.yml` - Updated to use ARM64 Dockerfile and removed obsolete version
- `frontend/e-commerce-app/Dockerfile` - Fixed npm install process
- `README.md` - Added troubleshooting section for ARM64 issues

## 🍎 ARM64 Optimizations

The `Dockerfile.arm64` includes these ARM64-specific fixes:

1. **Platform specification**: `FROM --platform=linux/arm64 node:20-alpine`
2. **npm configuration**: Sets target architecture and platform
3. **Force installation**: Uses `npm install --force` to handle dependency conflicts
4. **Additional build tools**: Installs python3, make, g++ for native modules
5. **Memory optimization**: Increases Node.js memory limit for builds

## 🔍 Verification

After running the fix, verify everything works:

```bash
# Check container status
docker-compose ps

# Test services
curl http://localhost:5000/health  # Auth Service
curl http://localhost:5001/health  # User Service
curl http://localhost:3000         # Frontend

# View logs if needed
docker-compose logs -f frontend
```

## 🛠️ If Issues Persist

### Common Additional Steps

1. **Restart Docker Desktop**:
   ```bash
   # Quit Docker Desktop completely, then restart it
   ```

2. **Clear all Docker data**:
   ```bash
   docker system prune -a --volumes
   docker-compose up --build -d
   ```

3. **Check available disk space**:
   ```bash
   docker system df
   ```

4. **Update dependencies**:
   ```bash
   cd frontend/e-commerce-app
   npm update
   npm audit fix
   ```

### Alternative Approach: Local Development

If Docker continues to have issues, you can run services locally:

```bash
# Follow the "Manual Local Setup" section in README.md
# This bypasses Docker entirely
```

## 📞 Support

- **Docker-specific issues**: Check [Docker Desktop troubleshooting](https://docs.docker.com/desktop/troubleshoot/)
- **ARM64/Apple Silicon**: Use `./scripts/fix-docker-issues.sh`
- **npm/Node.js issues**: Try updating to latest Node.js LTS

## ✅ Success Indicators

Your fix was successful when you see:
- ✅ All containers build without errors
- ✅ All services report healthy status
- ✅ Frontend accessible at http://localhost:3000
- ✅ APIs respond at http://localhost:5000 and http://localhost:5001

---

**Fixed! 🎉** Your e-commerce platform should now be running smoothly with Docker. 