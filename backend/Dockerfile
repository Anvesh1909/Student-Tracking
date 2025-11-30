FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for building / postgres client
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy code
COPY . /app

# Create a non-root user
RUN useradd --create-home appuser || true
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
ENV PORT=8000

ENTRYPOINT ["/app/entrypoint.sh"]
