import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch, MagicMock
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

@patch("telemetry_sensor.get_db_connection")
def test_reading_normal(mock_db, telemetry_client):
    """Værdi under 100 → NORMAL, status 200"""
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn
    res = telemetry_client.post("/reading", json={
        "sensor_id": 101, "value": 75.0, "unit": "dB", "turbine_speed": 45.5
    })
    assert res.status_code == 200
    assert res.get_json()["status"] == "Måling gemt"

@patch("telemetry_sensor.get_db_connection")
def test_reading_warning(mock_db, telemetry_client):
    """Værdi mellem 100-120 → ADVARSEL"""
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn
    res = telemetry_client.post("/reading", json={
        "sensor_id": 102, "value": 110.0, "unit": "dB", "turbine_speed": 62.3
    })
    assert res.status_code == 200

@patch("telemetry_sensor.get_db_connection")
def test_reading_critical(mock_db, telemetry_client):
    """Værdi over 120 → KRITISK"""
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn
    res = telemetry_client.post("/reading", json={
        "sensor_id": 201, "value": 130.0, "unit": "dB", "turbine_speed": 85.7
    })
    assert res.status_code == 200

def test_reading_missing_fields(telemetry_client):
    """Manglende felter → 400"""
    res = telemetry_client.post("/reading", json={"sensor_id": 101})
    assert res.status_code == 400

def test_reading_no_json(telemetry_client):
    """Ingen JSON → 400"""
    res = telemetry_client.post("/reading")
    assert res.status_code == 400

# --- Monitoring tests ---

@patch("monitoring_alerting.get_db_connection")
def test_anomaly_critical(mock_db, monitoring_client):
    """Severity >= 8 → KRITISK"""
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn
    res = monitoring_client.post("/anomaly", json={
        "sensor_id": 201,
        "description": "Kritisk temperaturstigning i gearkasse",
        "severity_score": 9
    })
    assert res.status_code == 200
    assert res.get_json()["asset_health"] == "KRITISK"

@patch("monitoring_alerting.get_db_connection")
def test_anomaly_warning(mock_db, monitoring_client):
    """Severity < 8 → ADVARSEL"""
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn
    res = monitoring_client.post("/anomaly", json={
        "sensor_id": 101,
        "description": "Unormal vibration på hovedleje",
        "severity_score": 6
    })
    assert res.status_code == 200
    assert res.get_json()["asset_health"] == "ADVARSEL"

def test_anomaly_missing_fields(monitoring_client):
    """Manglende felter → 400"""
    res = monitoring_client.post("/anomaly", json={"sensor_id": 101})
    assert res.status_code == 400