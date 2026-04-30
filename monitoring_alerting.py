from flask import Flask, request, jsonify
from db import get_db_connection

app = Flask(__name__)

@app.route("/anomaly", methods=["POST"])
def create_anomaly():
    data = request.get_json()
    if not data:
        return jsonify({"status": "Fejl", "error": "Ingen JSON data"}), 400

    sensor_id = data.get("sensor_id")
    description = data.get("description")
    severity_score = data.get("severity_score")
    if sensor_id is None:
        return jsonify({"status": "Fejl", "error": "Mangler sensor_id"}), 400
    if description is None:
        return jsonify({"status": "Fejl", "error": "Mangler description"}), 400
    if severity_score is None:
        return jsonify({"status": "Fejl", "error": "Mangler severity_score"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO anomalies (sensor_id, description, severity_score) VALUES (%s, %s, %s)",
            (
                sensor_id,
                description,
                severity_score,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        health = "KRITISK" if data.get("severity_score", 0) >= 8 else "ADVARSEL"
        return jsonify({"status": "Anomali logget", "asset_health": health})
    except Exception as e:
        return jsonify({"status": "Fejl", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True)
