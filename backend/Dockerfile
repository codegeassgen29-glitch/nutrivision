# Dockerfile (backend)
# ---------------------------------------------------------
# This file tells Docker how to build a "container image" for
# our backend - basically a snapshot of a mini computer that
# has Python + our libraries + our code, ready to run anywhere.
# ---------------------------------------------------------

# Start from an official, lightweight Python image.
# "slim" means it excludes extra OS tools we don't need,
# keeping the final image smaller and faster to download.
FROM python:3.11-slim

# Set the working directory INSIDE the container.
# Every command below runs relative to this folder.
WORKDIR /app

# Install system-level dependencies needed by psycopg2 (PostgreSQL driver)
# and, later, OpenCV. We do this before copying our code because
# system packages change far less often than our Python code does.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*
# Copy ONLY requirements.txt first (see explanation above the code block:
# this lets Docker cache the slow "pip install" step separately from
# our fast-changing application code).
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of our backend code into the container.
COPY . .

# Document that this container listens on port 8000.
# (This is informational for humans/tools; it doesn't actually
# open the port - that happens in docker-compose.yml)
EXPOSE 8000

# The command that runs when the container starts.
# --host 0.0.0.0 means "accept connections from outside the container"
# (not just from localhost inside it).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
