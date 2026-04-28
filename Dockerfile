FROM python:3.12-slim

# Installer OS-afhængigheder for pyodbc
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       g++ \
       unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PYTHONUNBUFFERED=1
CMD ["python3", "main.py"]
