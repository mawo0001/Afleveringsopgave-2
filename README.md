# Vindmølle Overvågningssystem

Dette projekt er en simpel vindmølleovervågning med følgende komponenter:

- `telemetry_sensor.py` — Flask API til at modtage telemetridata og gemme dem i databasen.
- `monitoring_alerting.py` — Flask API til at oprette anomalier i databasen.
- `app_dashboard.py` — Flask dashboard til at vise telemetri og anomalier.
- `simulator.py` — Sender testdata til `telemetry_sensor` og `monitoring_alerting`.
- `db.py` — Opretter forbindelse til Azure SQL via `pyodbc`.
- `Dockerfile` — Bygger et Python-image med Microsoft ODBC-driver.
- `docker-compose.yml` — Starter de fire services i én løsning.

## Kør projektet

1. Opret en `.env.local` med Azure SQL credentials:

```env
AZURE_SQL_USER=akse3585@stud.ek.dk
AZURE_SQL_PASSWORD=<din-password>
ODBC_DRIVER=ODBC Driver 18 for SQL Server
```

2. Start alle services med Docker Compose:

```bash
docker compose up --build
```

3. Åbn dashboardet i browseren:

```text
http://localhost:28080
```

## Serviceporte

- Dashboard: `28080:8080`
- Telemetry API: `25050:5050`
- Monitoring API: `25051:5051`

## Database

Projektet bruger Azure SQL. Sørg for at:

- `AZURE_SQL_PASSWORD` er korrekt sat i `.env.local`
- Azure SQL firewall tillader din IP eller "Allow Azure services"

## Bemærkninger

- Bevarer Flask API-arkitektur og Docker-setup.
- Der er ingen ændringer i komponenter eller services uden for de nødvendige filer.
- `sensor.py` er ikke længere brugt og er fjernet fra projektet.
