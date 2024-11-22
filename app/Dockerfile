# Use an official Python runtime as a parent image
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    build-essential \
    gcc \
    g++ \
    netcat-openbsd \
    dos2unix \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install stable requirements (this layer is cached unless requirements_stable.txt changes)
COPY requirements_stable.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_stable.txt

# Copy normal requirements file and install normal dependencies
# This will only run if requirements.txt changes
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Copy the entrypoint.sh script and make it executable
COPY ./entrypoint.sh /main-entrypoint.sh
# Convert line endings for entrypoint.sh
RUN dos2unix /main-entrypoint.sh

RUN chmod +x /main-entrypoint.sh

# Expose the application port
EXPOSE 8001

# Use entrypoint for the script
ENTRYPOINT ["/main-entrypoint.sh"]
