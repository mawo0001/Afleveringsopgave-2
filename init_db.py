import time
import psycopg2
from db import get_db_connection

def init_db(retries=10, delay=3):
    for attempt in range(retries):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensors (
                    id       INTEGER PRIMARY KEY,
                    name     TEXT NOT NULL,
                    location TEXT NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS readings (
                    id                 SERIAL PRIMARY KEY,
                    sensor_id          INTEGER NOT NULL,
                    value              REAL NOT NULL,
                    unit               TEXT NOT NULL,
                    turbine_speed      REAL DEFAULT 0,
                    severity           TEXT NOT NULL,
                    recommended_action TEXT NOT NULL,
                    timestamp          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anomalies (
                    id             SERIAL PRIMARY KEY,
                    sensor_id      INTEGER NOT NULL,
                    description    TEXT NOT NULL,
                    severity_score INTEGER NOT NULL,
                    timestamp      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Seed standard sensorer hvis de ikke allerede findes
            cursor.execute("SELECT COUNT(*) FROM sensors;")
            count = cursor.fetchone()
            if list(count.values())[0] == 0:
                cursor.execute("""
                    INSERT INTO sensors (id, name, location) VALUES
                    (101, 'Mølle-Nord-01', 'Hvide Sande'),
                    (102, 'Mølle-Nord-02', 'Hvide Sande'),
                    (201, 'Havmølle-Syd-A', 'Nordsøen');
                """)

            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Database initialiseret.")
            return
        except psycopg2.OperationalError:
            print(f"⏳ Venter på database... ({attempt + 1}/{retries})")
            time.sleep(delay)

    raise RuntimeError("❌ Kunne ikke forbinde til databasen efter flere forsøg.")

if __name__ == "__main__":
    init_db()