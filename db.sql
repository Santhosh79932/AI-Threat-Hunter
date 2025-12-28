-- Create table for raw network traffic
CREATE TABLE IF NOT EXISTS network_traffic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source_ip TEXT,
    dest_ip TEXT,
    packet_size INTEGER,
    duration FLOAT,
    protocol TEXT
);

-- Create table for flagged threats
CREATE TABLE IF NOT EXISTS detected_threats (
    threat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER,
    anomaly_score FLOAT,
    threat_level TEXT,
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (log_id) REFERENCES network_traffic(id)
);