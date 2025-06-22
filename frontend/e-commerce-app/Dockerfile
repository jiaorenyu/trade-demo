# ARM64-optimized React Frontend Dockerfile for macOS Apple Silicon
# Build stage
FROM --platform=linux/arm64 node:20-alpine AS builder

WORKDIR /app

# Install build dependencies for ARM64
RUN apk add --no-cache \
    curl \
    python3 \
    make \
    g++

# Set npm configurations for ARM64 compatibility
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV FORCE_COLOR=1

# Copy package files
COPY package*.json ./

# Clean npm cache and install dependencies with ARM64 optimizations
RUN npm cache clean --force && \
    npm ci --prefer-offline --no-audit --progress=false

# Copy source code
COPY . .

# Build application with ARM64 optimizations
RUN npm run build

# Production stage
FROM --platform=linux/arm64 nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 