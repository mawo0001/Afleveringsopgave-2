from flask import Flask, render_template
from db import get_db_connection

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Simpel landing page først - ingen database-forbindelse
    return """
    <h1>Vindmølle Overvågningssystem</h1>
    <p>Systemet er startet og kører.</p>
    <p><a href="/data">Se telemetri data</a></p>
    <p><a href="/test-db">Test database forbindelse</a></p>
    """

@app.route("/data")
def data_dashboard():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. HENT TELEMETRI (Målinger + Lokation)
        # Vi bruger en JOIN for at koble 'readings' sammen med 'sensors' via sensor_id
        query_readings = """
            SELECT 
                s.name, s.location, r.value, r.unit, r.turbine_speed, 
                r.severity, r.recommended_action, r.timestamp 
            FROM readings r
            JOIN sensors s ON s.id = r.sensor_id 
            ORDER BY r.timestamp DESC LIMIT 15
        """
        cursor.execute(query_readings)
        columns = [column[0] for column in cursor.description]
        readings_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # 2. HENT ALARMER (Anomalier)
        # Her henter vi beskrivelsen og scoren på fejlene
        query_anomalies = "SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 10"
        cursor.execute(query_anomalies)
        columns = [column[0] for column in cursor.description]
        anomalies_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        # Vi sender begge bunker data til vores HTML-skabelon
        return render_template("index.html", readings=readings_data, anomalies=anomalies_data)

    except Exception as e:
        # Hvis databasen ikke er tilgængelig, vis en fejl-side
        error_msg = f"""
        <h1>Database-forbindelsesfejl</h1>
        <p>Kan ikke oprette forbindelse til Azure SQL-database.</p>
        <p>Fejl: {str(e)}</p>
        <h2>Mulige løsninger:</h2>
        <ul>
            <li>Tjek at AZURE_SQL_PASSWORD er sat korrekt i .env.local</li>
            <li>Tjek Azure SQL firewall-regler - tillad din IP eller "Allow Azure services"</li>
            <li>Kontakt administrator for database-adgang</li>
        </ul>
        <p><a href="/">Tilbage til forsiden</a></p>
        """
        return error_msg

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"<h1>Database OK</h1><p>Test forespørgsel lykkedes: {result}</p><p><a href='/'>Tilbage</a></p>"
    except Exception as e:
        return f"<h1>Database Fejl</h1><p>{str(e)}</p><p><a href='/'>Tilbage</a></p>"

if __name__ == "__main__":
    print("Dashboardet kører! Gå til http://0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)
