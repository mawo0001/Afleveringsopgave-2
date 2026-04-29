import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from telemetry_sensor import app as telemetry_app
from monitoring_alerting import app as monitoring_app

@pytest.fixture
def telemetry_client():
    telemetry_app.config["TESTING"] = True
    with telemetry_app.test_client() as client:
        yield client

@pytest.fixture
def monitoring_client():
    monitoring_app.config["TESTING"] = True
    with monitoring_app.test_client() as client:
        yield client

# --- Telemetri tests ---

def test_reading_normal(telemetry_client):
    """Værdi under 100 → NORMAL"""
    res = telemetry_client.post("/reading", json={
        "id": 101, "value": 50.0, "unit": "Hz", "turbine_speed": 15.0
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["event"] == "TelemetryReceived"

def test_reading_critical(telemetry_client):
    """Værdi over 120 → KRITISK + GearboxVibrationExceeded"""
    res = telemetry_client.post("/reading", json={
        "id": 101, "value": 125.0, "unit": "Hz", "turbine_speed": 20.0
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["event"] == "GearboxVibrationExceeded"

def test_reading_missing_fields(telemetry_client):
    """Manglende felter → 500 fejl"""
    res = telemetry_client.post("/reading", json={"id": 101})
    assert res.status_code == 500

# --- Monitoring tests ---

def test_anomaly_critical(monitoring_client):
    """Severity >= 8 → KRITISK"""
    res = monitoring_client.post("/anomaly", json={
        "sensor_id": 101,
        "description": "Høj vibration",
        "severity_score": 9
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["asset_health"] == "KRITISK"

def test_anomaly_warning(monitoring_client):
    """Severity < 8 → ADVARSEL"""
    res = monitoring_client.post("/anomaly", json={
        "sensor_id": 101,
        "description": "Moderat vibration",
        "severity_score": 5
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["asset_health"] == "ADVARSEL"