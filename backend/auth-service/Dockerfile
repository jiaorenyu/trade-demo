# ARM64-optimized Authentication Service Dockerfile for macOS Apple Silicon
FROM --platform=linux/arm64 python:3.11-alpine

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

# Install Python dependencies individually to avoid conflicts
RUN pip install --no-cache-dir \
    Flask==3.1.1 \
    Flask-RESTful==0.3.10 \
    Flask-JWT-Extended==4.7.1 \
    marshmallow==4.0.0 \
    SQLAlchemy==2.0.41 \
    psycopg2-binary==2.9.10 \
    python-dotenv==1.1.0 \
    werkzeug==3.1.3 \
    requests==2.31.0

# Copy application code
COPY . .

# Use simplified auth service to avoid email conflicts
RUN cp app_simple.py app.py || echo "Using existing app.py"

# Create non-root user
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=45s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["python", "app.py"] 