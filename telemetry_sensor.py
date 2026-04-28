from flask import Flask, request, jsonify
from sensor import SensorReading, SensorEndpoint
from db import get_db_connection

app = Flask(__name__)

@app.route("/reading", methods=["POST"])
def receive_reading():
    data = request.get_json()
    val = data["value"]
    
    # Logik til at bestemme alvorlighed og handling
    if val > 120:
        sev = "KRITISK"
        act = "NØDSTOP: Kontakt tekniker straks!"
    elif val > 100:
        sev = "ADVARSEL"
        act = "Planlæg eftersyn indenfor 24 timer"
    else:
        sev = "NORMAL"
        act = "Ingen handling påkrævet"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Gem alt i databasen inkl. de nye felter
        query = """
            INSERT INTO readings (sensor_id, value, unit, turbine_speed, severity, recommended_action) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (data["id"], val, data["unit"], data.get("turbine_speed", 0), sev, act))
        
        conn.commit()
        cursor.close()
        conn.close()

        event = "GearboxVibrationExceeded" if data["value"] > 100 else "TelemetryReceived"
        return jsonify({"status": "Måling gemt", "event": event})
        
    except Exception as e:
        return jsonify({"status": "Fejl", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5050, debug=True)