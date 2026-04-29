from flask import Flask, render_template
from db import get_db_connection

app = Flask(__name__)

@app.route("/")
def dashboard():
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
        readings_data = []
        for row in cursor.fetchall():
            r = dict(row)
            r['value'] = float(r['value'])
            r['turbine_speed'] = float(r['turbine_speed']) if r['turbine_speed'] else 0.0
            readings_data.append(r)
        
        query_anomalies = "SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 10"
        cursor.execute(query_anomalies)
        anomalies_data = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return render_template("index.html", readings=readings_data, anomalies=anomalies_data)

    except Exception as e:
        return f"Der skete en fejl i dashboardet: {e}"

if __name__ == "__main__":
    print("Dashboardet kører! Gå til http://127.0.0.1:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)