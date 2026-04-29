# 📋 FILE AUDIT REPORT

## ✅ FILER MED FUNKTION

| Fil | Funktion | Status |
|-----|----------|--------|
| `db.py` | PostgreSQL connection | ✅ Brugt |
| `telemetry_sensor.py` | Flask API (port 5050) | ✅ Brugt |
| `monitoring_alerting.py` | Flask API (port 5051) | ✅ Brugt |
| `app_dashboard.py` | Flask dashboard (port 8080) | ✅ Brugt |
| `simulator.py` | Test data generator | ✅ Brugt |
| `docker-compose.yml` | Orchestration af alle services | ✅ Brugt |
| `Dockerfile` | Container image builder | ✅ Brugt |
| `requirements.txt` | Python dependencies | ✅ Brugt |
| `init-db.sql` | Database schema + seed data | ✅ Brugt |
| `.env.local` | Development miljøvariabler | ✅ Brugt |
| `.gitignore` | Beskytter secrets | ✅ Brugt |
| `.dockerignore` | Ekskluderer filer fra image | ✅ Brugt |
| `templates/index.html` | Dashboard HTML/CSS | ✅ Brugt |
| `README.md` | Opsætningsvejledning | ✅ Brugt |
| `ARCHITECTURE.md` | System design dokumentation | ✅ Brugt |
| `SECURITY_REVIEW.md` | Security audit | ✅ Brugt |

## 🔴 UNØDVENDIGE FILER - SKAL SLETTES

| Fil | Grund | Handling |
|-----|-------|----------|
| `main.py` | Gammel orchestration (before Docker) | ❌ DELETE |
| `python` | Tom fil, ingen funktion | ❌ DELETE |
| `config.yml` | Ikke brugt af kode (kun dokumentation) | ⚠️ VALGFRIT |

### `main.py` - Hvorfor det skal slettes?
- **Før**: Var usado til at starte alle scripts lokalt uden Docker
- **Nu**: Docker-compose gør dette job bedre
- **Problem**: Kan forvirre at der er 2 måder at starte systemet på
- **Bedst praksis**: Med Docker er bare `docker compose up`

### `python` - Hvorfor det skal slettes?
- Filen er **100% tom**
- Ingen funktion
- Bare noise i repo

### `config.yml` - Skal den slettes?
- **Argument FOR at beholde**: Dokumentation af config struktur
- **Argument FOR at slette**: Ikke brugt af Python, bare template
- **Anbefaling**: BEHOLDE som reference + dokumentation

## 💡 KODE CHECK

### Python kode
- ✅ Alle imports er valide
- ✅ Ingen dead code
- ✅ SQL queries er parameteriserede
- ✅ Error handling på alle DB-calls

### Filer der mangler (og det er OK)
- ❌ `.env.prod` - Den skal ikke være versioneret (på .gitignore)
- ❌ `venv/` - Skal ikke være versioneret (på .gitignore)
- ❌ `__pycache__/` - Skal ikke være versioneret (på .gitignore)
- ❌ `postgres_data/` - Skal ikke være versioneret (på .gitignore)

## 🎯 RECOMMENDATION

**DELETE**:
```bash
rm main.py python
```

**KEEP**:
- Alle andre filer har formål

**Result**: Cleanere repo, mindre forvirring! ✨
