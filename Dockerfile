# Dockerfile
FROM python:3.10-slim

# Avoids prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

WORKDIR /app

# system deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# copy project
COPY . /app

# install python deps
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE ${PORT}

# Run with gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers", "2"]
