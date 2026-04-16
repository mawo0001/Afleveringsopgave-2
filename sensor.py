from dataclasses import dataclass

# Definerer EN aflæsning fra en sensor (Value Object)
@dataclass
class SensorReading:
    value: float
    unit: str
    turbine_speed: float  # Tilføjet for at måle omdrejninger

# Definerer EN sensor i systemet (Entity)
@dataclass
class SensorEndpoint:
    id: int
    name: str
    location: str

# Definerer EN anomali der er opdaget (Entity)
@dataclass
class AnomalyHistory:
    sensor_id: int
    description: str
    severity_score: int  # 1-10

# --- Testdata ---
# Her opretter vi nogle standard eksempler, så systemet har noget at starte på
test_sensor = SensorEndpoint(id=1, name="Gearbox Sensor A", location="Hall 1")

# VIGTIGT: Her har vi nu tilføjet turbine_speed=80.0 for at matche klassen ovenfor
test_reading = SensorReading(value=120.0, unit="Hz", turbine_speed=80.0)

test_anomaly = AnomalyHistory(sensor_id=1, description="Høj vibration registreret", severity_score=9)