-- Create tables for Windmill Monitoring System

-- Create sensors table
CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    sensor_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create readings table (telemetry data)
CREATE TABLE IF NOT EXISTS readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL,
    value FLOAT NOT NULL,
    unit VARCHAR(50),
    turbine_speed FLOAT,
    severity VARCHAR(50),
    recommended_action TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);

-- Create anomalies table
CREATE TABLE IF NOT EXISTS anomalies (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL,
    description TEXT,
    severity_score INTEGER,
    status VARCHAR(50) DEFAULT 'OPEN',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_readings_sensor_id ON readings(sensor_id);
CREATE INDEX IF NOT EXISTS idx_readings_timestamp ON readings(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_anomalies_sensor_id ON anomalies(sensor_id);
CREATE INDEX IF NOT EXISTS idx_anomalies_timestamp ON anomalies(timestamp DESC);

-- Insert sample sensor data
INSERT INTO sensors (id, name, location, sensor_type) VALUES
    (101, 'Mølle-Nord-01', 'Hvide Sande', 'vibration'),
    (102, 'Mølle-Nord-02', 'Hvide Sande', 'vibration'),
    (201, 'Havmølle-Syd-A', 'Nordsøen', 'vibration')
ON CONFLICT DO NOTHING;

-- Create logs table for monitoring
CREATE TABLE IF NOT EXISTS system_logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(50),
    message TEXT,
    component VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON system_logs(timestamp DESC);
