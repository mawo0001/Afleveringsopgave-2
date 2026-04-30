from flask import Flask, request, jsonify
from db import get_db_connection

app = Flask(__name__)

@app.route("/reading", methods=["POST"])
def receive_reading():
    data = request.get_json()
    if not data:
        return jsonify({"status": "Fejl", "error": "Ingen JSON data"}), 400

    sensor_id = data.get("sensor_id")
    value = data.get("value")
    if sensor_id is None:
        return jsonify({"status": "Fejl", "error": "Mangler sensor_id"}), 400
    if value is None:
        return jsonify({"status": "Fejl", "error": "Mangler value"}), 400

    if value > 120:
        severity = "KRITISK"
        action = "NØDSTOP: Kontakt tekniker straks!"
    elif value > 100:
        severity = "ADVARSEL"
        action = "Planlæg eftersyn indenfor 24 timer"
    else:
        severity = "NORMAL"
        action = "Ingen handling påkrævet"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO readings (sensor_id, value, unit, turbine_speed, severity, recommended_action)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                sensor_id,
                value,
                data.get("unit"),
                data.get("turbine_speed", 0),
                severity,
                action,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "Måling gemt"})
    except Exception as e:
        return jsonify({"status": "Fejl", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
