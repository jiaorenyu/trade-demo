#!/bin/bash

# Quick Fix Script - Start Docker and Fix Everything
echo "🚀 Quick Fix: Starting Docker and Building Platform"
echo "================================================="

# Start Docker Desktop
echo "1️⃣ Starting Docker Desktop..."
open -a Docker

echo "2️⃣ Waiting for Docker to start..."
for i in {1..30}; do
    if docker info >/dev/null 2>&1; then
        echo "✅ Docker is running!"
        break
    fi
    echo "   Waiting for Docker... ($i/30)"
    sleep 2
done

# Check if Docker started
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker failed to start automatically."
    echo "📱 Please start Docker Desktop manually, then run:"
    echo "   ./scripts/fix-docker-issues.sh"
    exit 1
fi

echo "3️⃣ Running comprehensive fix..."
./scripts/fix-docker-issues.sh

echo "🎉 Quick fix completed!" 