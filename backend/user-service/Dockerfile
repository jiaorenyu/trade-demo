# ARM64-optimized User Service Dockerfile for macOS Apple Silicon
FROM --platform=linux/arm64 python:3.11-alpine

# Set working directory
WORKDIR /app

# Install system dependencies optimized for ARM64
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    curl \
    libffi-dev

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=45s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Start application
CMD ["python", "app.py"] 