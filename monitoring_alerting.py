from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from db import get_db_connection

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'monitoring_requests_total',
    'Total number of monitoring requests',
    ['endpoint', 'method', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'monitoring_request_duration_seconds',
    'Monitoring request duration in seconds',
    ['endpoint']
)

@app.route("/anomaly", methods=["POST"])
def create_anomaly():
    start_time = time.time()
    data = request.get_json()
    if not data:
        REQUEST_COUNT.labels(endpoint='/anomaly', method='POST', http_status='400').inc()
        return jsonify({"status": "Fejl", "error": "Ingen JSON data"}), 400

    sensor_id = data.get("sensor_id")
    description = data.get("description")
    severity_score = data.get("severity_score")
    if sensor_id is None:
        REQUEST_COUNT.labels(endpoint='/anomaly', method='POST', http_status='400').inc()
        return jsonify({"status": "Fejl", "error": "Mangler sensor_id"}), 400
    if description is None:
        REQUEST_COUNT.labels(endpoint='/anomaly', method='POST', http_status='400').inc()
        return jsonify({"status": "Fejl", "error": "Mangler description"}), 400
    if severity_score is None:
        REQUEST_COUNT.labels(endpoint='/anomaly', method='POST', http_status='400').inc()
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

        health = "KRITISK" if severity_score >= 8 else "ADVARSEL"
        REQUEST_LATENCY.labels(endpoint='/anomaly').observe(time.time() - start_time)
        REQUEST_COUNT.labels(endpoint='/anomaly', method='POST', http_status='200').inc()
        return jsonify({"status": "Anomali logget", "asset_health": health})
    except Exception as e:
        REQUEST_COUNT.labels(endpoint='/anomaly', method='POST', http_status='500').inc()
        return jsonify({"status": "Fejl", "error": str(e)}), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True)
