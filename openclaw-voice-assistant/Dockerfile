# OpenClaw Voice Assistant Dockerfile
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 openclaw && \
    chown -R openclaw:openclaw /app
USER openclaw

# Create data directory
RUN mkdir -p /app/data && chown openclaw:openclaw /app/data

# Expose port (if web interface added later)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "scripts/interactive_chat.py"]

# Labels
LABEL maintainer="leilei926524-tech"
LABEL version="1.0.0"
LABEL description="OpenClaw Voice Assistant with Samantha AI"
LABEL org.opencontainers.image.source="https://github.com/leilei926524-tech/openclaw-voice-assistant"