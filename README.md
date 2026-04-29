# Vindmølle Overvågningssystem

Vindmølleovervågningssystem med PostgreSQL database, Docker containerization og sikker miljøvariabel-håndtering.

## 🏗️ Systemarkitektur

Systemet består af følgende komponenter:

| Komponent | Port | Beskrivelse |
|-----------|------|-------------|
| **PostgreSQL Database** | 5432 | Holder alle sensor-data, aflæsninger og anomalier |
| **Telemetry API** | 5050 | Flask API til at modtage sensor-telemetri |
| **Monitoring & Alerting** | 5051 | Flask API til at registrere anomalier |
| **Dashboard** | 8080 | Flask web dashboard til datavisning |
| **Simulator** | - | Genererer testdata til systemet |

## 📋 Filer

- `db.py` — PostgreSQL database-forbindelsesmodul
- `telemetry_sensor.py` — Flask API (port 5050) til að modtage måledata
- `monitoring_alerting.py` — Flask API (port 5051) til at logge anomalier
- `app_dashboard.py` — Flask dashboard (port 8080) til visualisering
- `simulator.py` — Test-data generator der sender data videre
- `Dockerfile` — Multi-layer container image for Python-applikation
- `docker-compose.yml` — Orkestrer alle services med PostgreSQL
- `config.yml` — Applikationskonfiguration
- `init-db.sql` — Databaseinitialisering med tabeller og indexes

## 🚀 Hurtig start

### Forudsætninger
- Docker & Docker Compose
- git (anbefalet)

### Installation & Kørsel

1. **Klon/download projektet:**
```bash
cd /path/to/Afleveringsopgave-2-main
```

2. **Start alle services:**
```bash
docker compose up --build
```

Docker vil automatisk:
- Starte PostgreSQL og initialisere databasen med `init-db.sql`
- Bygge Python-image'et
- Starte alle 5 services i korrekt rækkefølge
- Oprette netværk for intern kommunikation

3. **Åbn dashboardet:**
```
http://localhost:8080
```

4. **Tjek telemetri data:**
```
http://localhost:8080/data
```

## 🔧 Miljøvariabler

Konfigureres i `.env.local` (allerede lavet):

```env
# PostgreSQL
POSTGRES_HOST=postgresql
POSTGRES_PORT=5432
POSTGRES_DB=vindmolle_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

**⚠️ SIKKERHED:** `.env.local` og `.env.prod` er på `.gitignore` - dine secrets er sikre!

## 📊 Database-skema

### `sensors` tabel
```sql
id | name | location | sensor_type | created_at
```

### `readings` tabel
```sql
id | sensor_id | value | unit | turbine_speed | severity | recommended_action | timestamp
```

### `anomalies` tabel
```sql
id | sensor_id | description | severity_score | status | timestamp
```

Alle tabeller har passende indexes for performance.

## 🔌 API Endpoints

### Telemetry (port 5050)
```bash
POST /reading
{
  "id": 101,
  "value": 95.5,
  "unit": "Hz",
  "turbine_speed": 18.5
}
```

### Monitoring (port 5051)
```bash
POST /anomaly
{
  "sensor_id": 101,
  "description": "High vibration detected",
  "severity_score": 8
}
```

### Dashboard (port 8080)
```bash
GET /          # Startside
GET /data      # Telemetri & anomalier fra database
```

## 🛑 Stop systemet

```bash
docker compose down
```

For at slette database-data også:
```bash
docker compose down -v
```

## 📝 Udvikling lokalt (uden Docker)

1. Opret virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Installer dependencies:
```bash
pip install -r requirements.txt
```

3. Start PostgreSQL eksternt (lokal server eller anden host)

4. Sæt miljøvariabler:
```bash
export POSTGRES_HOST=localhost
export POSTGRES_PASSWORD=ditt_passord
```

5. Kør hver service individuelt:
```bash
python3 telemetry_sensor.py
python3 monitoring_alerting.py
python3 app_dashboard.py
python3 simulator.py  # I en anden terminal
```

## 🔐 Sikkerhed

- ✅ `.env` filer på `.gitignore` — hemmeligheder committed aldrig til git
- ✅ PostgreSQL kræver password-autentificering
- ✅ Docker container-isolation mellem services
- ✅ SQL-injection beskyttelse via parameteriserede queries

## 🐛 Fejlfinding

**Kan ikke forbinde til database?**
```bash
docker compose logs postgres
```

**Flask-app starter ikke?**
```bash
docker compose logs dashboard
docker compose logs telemetry
```

**Data vises ikke?**
Tjek at `init-db.sql` blev kørt. Manuelt:
```bash
docker compose exec postgres psql -U postgres -d vindmolle_db -f /docker-entrypoint-initdb.d/init.sql
```

**Slet alt og genstart:**
```bash
docker compose down -v
docker system prune -a
docker compose up --build
```

## 📚 Ressourcer

- [Docker Compose docs](https://docs.docker.com/compose/)
- [PostgreSQL docs](https://www.postgresql.org/docs/)
- [psycopg2 docs](https://www.psycopg.org/)
- [Flask docs](https://flask.palletsprojects.com/)
