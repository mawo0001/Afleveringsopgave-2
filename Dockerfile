FROM python:3.12-slim

# Installer OS-afhængigheder og Microsoft ODBC-driver til Azure SQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       gnupg2 \
       ca-certificates \
       gcc \
       g++ \
       unixodbc-dev \
       gpg \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg \
    && curl -sSL https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PYTHONUNBUFFERED=1
CMD ["python3", "main.py"]
