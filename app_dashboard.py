from flask import Flask, render_template, redirect, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from db import get_db_connection

app = Flask(__name__)

@app.route("/")
def dashboard():
    return redirect("/data")

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

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
