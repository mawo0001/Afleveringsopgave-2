import subprocess
import time
import sys

def start_system():
    print("🏗️  Starter Vindmølle Overvågningssystemet...")
    
    processes = []
    
    # Liste over alle dine scripts
    scripts = [
        "telemetry_sensor.py",   # Port 5050
        "monitoring_alerting.py", # Port 5051
        "app_dashboard.py"       # Port 8080
    ]

    try:
        # 1. Start alle server-services først
        for script in scripts:
            print(f"🚀 Starter {script}...")
            proc = subprocess.Popen([sys.executable, script])
            processes.append(proc)
            time.sleep(2)  # Vent lidt så portene når at åbne

        print("\n🖥️  Alle servere kører!")
        print("🔗 Dashboard: http://127.0.0.1:8080")
        print("------------------------------------------")

        # 2. Start simulatoren sidst
        print("⚙️  Starter simulatoren (Data-generering)...")
        sim_proc = subprocess.Popen([sys.executable, "simulator.py"])
        processes.append(sim_proc)

        print("\n✅ SYSTEMET KØRER. Tryk Ctrl+C for at lukke alt på én gang.\n")

        # Hold main.py kørende så længe processerne lever
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Lukker systemet ned...")
        for proc in processes:
            proc.terminate() # Dræber hver enkelt proces pænt
        print("👋 Alt er lukket. Vi ses!")

if __name__ == "__main__":
    start_system()