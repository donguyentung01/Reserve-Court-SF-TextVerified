# Use an official Python runtime as a base image
FROM python:3.9-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libx11-dev \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgdk-pixbuf2.0-0 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Set the environment variable to use Chromium

# Command to run the Python script
ENTRYPOINT ["python3", "main.py"]

