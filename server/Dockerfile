# Use Python 3.11
FROM python:3.11-silm

# Prevent Python from creating .pyc files
ENV PYTHONUNBUFFERED=1
# Send Python output directly to the terminal
ENV PYTHONDONTWRITEBYTECODE=1

# Install uv
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

#  Set working directory
WORKDIR /app

# to update server/docter instances
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first
# This allows Docker to cache dependencies
# COPY pyproject.toml uv.lock ./

# Install dependencies into the container
# RUN uv sync --frozen --no-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . .

# Django runs on port 8000
EXPOSE 8000

# Start Django
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "180"]
