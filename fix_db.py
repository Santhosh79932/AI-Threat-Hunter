import sqlite3
import os

# Use a consistent path across all files
DB_PATH = 'db/threat_hunter.db'

if not os.path.exists('db'):
    os.makedirs('db')

def init():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create the traffic table
        cursor.execute('''CREATE TABLE IF NOT EXISTS network_traffic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_ip TEXT,
            packet_size INTEGER,
            duration REAL
        )''')
        
        # Create the results table
        cursor.execute('''CREATE TABLE IF NOT EXISTS detected_threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_id INTEGER,
            anomaly_score REAL,
            threat_level TEXT
        )''')
        
        conn.commit()
        print("✅ Database initialized successfully at db/threat_hunter.db")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init()