FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set work directory
WORKDIR /app

# Copy uv configuration files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ ./src/

# Create non-root user with home directory
RUN groupadd -r appuser && useradd -r -g appuser -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Set environment variables for the user
ENV UV_CACHE_DIR=/home/appuser/.cache/uv

# Expose port (if needed for health checks)
EXPOSE 8080

# Set default command
CMD ["uv", "run", "python", "-m", "fmp_mcp_server.server"]