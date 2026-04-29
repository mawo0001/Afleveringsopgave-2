FROM python:3.12-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PYTHONUNBUFFERED=1
CMD ["python3", "main.py"]
