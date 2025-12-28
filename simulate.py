import sqlite3
import random

DB_PATH = 'db/threat_hunter.db'

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Normal packets
    for _ in range(100):
        cursor.execute("INSERT INTO network_traffic (source_ip, packet_size, duration) VALUES (?, ?, ?)",
                       ('192.168.1.5', random.randint(50, 500), random.uniform(0.1, 1.0)))
        
    # Anomaly packets (High volume/Duration)
    for _ in range(5):
        cursor.execute("INSERT INTO network_traffic (source_ip, packet_size, duration) VALUES (?, ?, ?)",
                       ('10.0.0.99', random.randint(10000, 50000), random.uniform(10.0, 50.0)))
        
    conn.commit()
    conn.close()
    print("✅ Database seeded with 105 rows of traffic.")

if __name__ == "__main__":
    seed_data()