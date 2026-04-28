from flask import Flask, render_template
from db import get_db_connection

app = Flask(__name__)

@app.route("/")
def dashboard():
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
        # Hvis databasen mangler en kolonne (f.eks. turbine_speed), vil fejlen vises her
        return f"Der skete en fejl i dashboardet: {e}"

if __name__ == "__main__":
    print("Dashboardet kører! Gå til http://127.0.0.1:8080")
    app.run(port=8080, debug=True)
