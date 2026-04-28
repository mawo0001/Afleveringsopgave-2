from flask import Flask, request, jsonify
from sensor import AnomalyHistory, SensorEndpoint
from db import get_db_connection  # <--- RETTET HER

app = Flask(__name__)

@app.route("/anomaly", methods=["POST"])
def create_anomaly():
    data = request.get_json()
    
    # Opret forbindelse ved hjælp af det rigtige funktionsnavn
    conn = get_db_connection() # <--- RETTET HER
    cursor = conn.cursor()
    
    # Gem anomalien i databasen
    cursor.execute(
        "INSERT INTO anomalies (sensor_id, description, severity_score) VALUES (?, ?, ?)",
        (data["sensor_id"], data["description"], data["severity_score"])
    )
    
    conn.commit()
    cursor.close()
    conn.close()

    health = "KRITISK" if data["severity_score"] >= 8 else "ADVARSEL"
    return jsonify({"status": "Anomali logget i database", "asset_health": health})

if __name__ == "__main__":
    app.run(port=5051, debug=True)
