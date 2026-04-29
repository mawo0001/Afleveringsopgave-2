import requests
import time
import random

# Adresserne på dine to Flask-services
TELEMETRY_URL = "http://telemetry:5050/reading"
ALARM_URL = "http://monitoring:5051/anomaly"

# Definition af vores test-møller
turbines = [
    {"id": 101, "name": "Mølle-Nord-01", "location": "Hvide Sande"},
    {"id": 102, "name": "Mølle-Nord-02", "location": "Hvide Sande"},
    {"id": 201, "name": "Havmølle-Syd-A", "location": "Nordsøen"}
]

def run_simulation():
    print("🚀 Simulatoren er startet... Tryk Ctrl+C for at stoppe.")
    
    while True:
        for turbine in turbines:
            # Generer tilfældige data
            vibration = round(random.uniform(20.0, 130.0), 2)
            speed = round(random.uniform(10.0, 25.0), 2)
            
            # 1. Saml data til telemetri
            payload = {
                "id": turbine["id"],
                "name": turbine["name"],
                "location": turbine["location"],
                "value": vibration,
                "unit": "Hz",
                "turbine_speed": speed
            }

            try:
                # Send måling
                requests.post(TELEMETRY_URL, json=payload)
                print(f"✅ Sendt måling for {turbine['name']}: {vibration} Hz")

                # 2. Hvis vibrationen er for høj, send en anomali-alarm
                if vibration > 110:
                    alarm_payload = {
                        "sensor_id": turbine["id"],
                        "description": f"Kritisk vibration registreret ved {speed} RPM",
                        "severity_score": random.randint(8, 10),
                        "turbine_speed": speed,
                        "location": turbine["location"]
                    }
                    requests.post(ALARM_URL, json=alarm_payload)
                    print(f"⚠️ ALARM SENDT for {turbine['name']}!")

            except Exception as e:
                print(f"❌ Kunne ikke forbinde: {e}")

        time.sleep(5) # Vent 5 sekunder

if __name__ == "__main__":
    run_simulation()