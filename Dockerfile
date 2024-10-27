FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    postgresql-dev \
    libpq

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . /app/

RUN adduser -D appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app/staticfiles /app/media

USER appuser
