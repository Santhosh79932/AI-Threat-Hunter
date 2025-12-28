import sqlite3
import pandas as pd
from detector import ThreatDetector

DB_PATH = 'db/threat_hunter.db'

def run_threat_hunt():
    conn = sqlite3.connect(DB_PATH)
    
    query = "SELECT * FROM network_traffic"
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("❌ No logs found. Run simulate.py first.")
        return

    # Run ML Detection
    detector = ThreatDetector(contamination=0.1)
    detector.train(df)
    preds, scores = detector.predict(df)
    
    df['anomaly'] = preds
    df['score'] = scores

    cursor = conn.cursor()
    # Clear old threats before saving new ones
    cursor.execute("DELETE FROM detected_threats")
    
    threats_found = 0
    # Isolation Forest marks anomalies as -1
    for index, row in df[df['anomaly'] == -1].iterrows():
        threat_level = "High" if row['score'] < -0.1 else "Medium"
        cursor.execute('''
            INSERT INTO detected_threats (log_id, anomaly_score, threat_level)
            VALUES (?, ?, ?)
        ''', (row['id'], row['score'], threat_level))
        threats_found += 1
    
    conn.commit()
    print(f"🎯 Hunt Complete: {threats_found} threats identified and logged to SQL.")
    conn.close()

if __name__ == "__main__":
    run_threat_hunt()