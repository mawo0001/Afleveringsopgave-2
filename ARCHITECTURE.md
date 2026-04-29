# 🏗️ Systemarkitektur - PostgreSQL Vindmølleovervågning

## Applikation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   DOCKER COMPOSE NETWORK                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │  Simulator   │─────→│ Telemetry    │                    │
│  │  (Generator) │      │ API (5050)   │                    │
│  │              │─────→│              │                    │
│  └──────────────┘      └──────────────┘                    │
│                               │                             │
│                        ┌──────▼───────┐                    │
│  ┌──────────────┐      │              │                    │
│  │  Monitoring  │◄──────│  PostgreSQL  │  ← INSERT readings│
│  │ + Alerting   │      │  Database    │  ← INSERT anomaly │
│  │  API (5051)  │      │  (Port 5432) │  ← SELECT for dash│
│  └──────────────┘      │              │                    │
│         │              └──────▲───────┘                    │
│         │                     │                             │
│         └─────────────────────┘                            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Flask Dashboard (8080)                      │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │ GET /data → Query DB → Render HTML           │    │  │
│  │  │ Display: Sensor telemetri + Anomalies        │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Simulator** genererer tilfældig sensor-data hver 5 sekund
2. **Telemetry API** modtager POST-requests med måledata
3. **Data gemmes i PostgreSQL** med timestamp, sensor-id, og værdi
4. **Monitoring API** sender anomali-meldinger hvis værdi > 110
5. **Dashboard** læser fra database og viser HTML med seneste data

## Sikkerhed & Bedste Praksis

✅ **Hemmeligheder**
- Environment variables i `.env.local`
- `.gitignore` sikrer hemmeligheder ikke committed
- Separat `.env.prod` for production

✅ **Database**
- PostgreSQL med password-auth
- SQL-injection beskyttelse via `psycopg2` parameterisering
- Tabel-indexes for performance

✅ **Docker**
- Multi-stage image (kun nødvendige packages)
- Network isolation mellem containers
- Health checks for databse
- Volume for persistent data

✅ **Fejlhåndtering**
- Try-catch omkring alle DB-operationer
- HTTP 400/500 error responses
- Connection pooling via `psycopg2`

## Opsætning Checklist

- [x] PostgreSQL i docker-compose.yml
- [x] init-db.sql med skema og seed-data
- [x] .env.local for local development
- [x] db.py konverteret til psycopg2
- [x] SQL queries opdateret til PostgreSQL syntax (%s placeholder)
- [x] Dockerfile optimeret (ingen Azure ODBC)
- [x] .gitignore beskytter hemmeligheder
- [x] README med fuldt opsætningsvejledning
- [x] docker-compose.yml med ord nursing af services

## Kørsel

```bash
# Start alt
docker compose up --build

# Åbn dashboard
open http://localhost:8080/data

# Se logs
docker compose logs -f

# Stop alt
docker compose down
```

Done! ✨
