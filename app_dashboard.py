from flask import Flask, render_template
from db import get_db_connection

app = Flask(__name__)

@app.route("/")
def dashboard():
    return """
    <h1>Vindmølle Overvågningssystem</h1>
    <p><a href="/data">Se telemetri og alarmer</a></p>
    """

@app.route("/data")
def data_dashboard():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

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

        query_anomalies = "SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 10"
        cursor.execute(query_anomalies)
        columns = [column[0] for column in cursor.description]
        anomalies_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        conn.close()
        return render_template("index.html", readings=readings_data, anomalies=anomalies_data)

    except Exception as e:
        return f"""
        <h1>Database-fejl</h1>
        <p>{str(e)}</p>
        <p><a href='/'>Tilbage</a></p>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
