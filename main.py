import subprocess
import time
import sys
from init_db import init_db

def start_system():
    print("🏗️  Starter Vindmølle Overvågningssystemet...")

    # Initialiser databasen før alt andet
    print("🗄️  Initialiserer database...")
    init_db()

    processes = []

    scripts = [
        "telemetry_sensor.py",    # Port 5050
        "monitoring_alerting.py", # Port 5051
        "app_dashboard.py"        # Port 8080
    ]

    try:
        for script in scripts:
            print(f"🚀 Starter {script}...")
            proc = subprocess.Popen([sys.executable, script])
            processes.append(proc)
            time.sleep(2)

        print("\n🖥️  Alle servere kører!")
        print("🔗 Dashboard:          http://127.0.0.1:8080")
        print("🔗 Telemetri API:      http://127.0.0.1:5050/reading")
        print("🔗 Monitoring API:     http://127.0.0.1:5051/anomaly")
        print("------------------------------------------")

        print("⚙️  Starter simulatoren (data-generering)...")
        sim_proc = subprocess.Popen([sys.executable, "simulator.py"])
        processes.append(sim_proc)

        print("\n✅ SYSTEMET KØRER. Tryk Ctrl+C for at lukke alt.\n")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Lukker systemet ned...")
        for proc in processes:
            proc.terminate()
        print("👋 Alt er lukket. Vi ses!")

if __name__ == "__main__":
    start_system()