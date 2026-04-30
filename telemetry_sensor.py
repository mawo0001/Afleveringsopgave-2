from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from db import get_db_connection

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'telemetry_requests_total',
    'Total number of telemetry requests',
    ['endpoint', 'method', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'telemetry_request_duration_seconds',
    'Telemetry request duration in seconds',
    ['endpoint']
)

@app.route("/reading", methods=["POST"])
def receive_reading():
    start_time = time.time()
    data = request.get_json()
    if not data:
        REQUEST_COUNT.labels(endpoint='/reading', method='POST', http_status='400').inc()
        return jsonify({"status": "Fejl", "error": "Ingen JSON data"}), 400

    sensor_id = data.get("sensor_id")
    value = data.get("value")
    if sensor_id is None:
        REQUEST_COUNT.labels(endpoint='/reading', method='POST', http_status='400').inc()
        return jsonify({"status": "Fejl", "error": "Mangler sensor_id"}), 400
    if value is None:
        REQUEST_COUNT.labels(endpoint='/reading', method='POST', http_status='400').inc()
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
        REQUEST_LATENCY.labels(endpoint='/reading').observe(time.time() - start_time)
        REQUEST_COUNT.labels(endpoint='/reading', method='POST', http_status='200').inc()
        return jsonify({"status": "Måling gemt"})
    except Exception as e:
        REQUEST_COUNT.labels(endpoint='/reading', method='POST', http_status='500').inc()
        return jsonify({"status": "Fejl", "error": str(e)}), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
