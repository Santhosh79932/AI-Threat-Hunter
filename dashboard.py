import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="AI Threat Hunter Dashboard", layout="wide")

st.title("🛡️ AI-Powered Threat Hunting Dashboard")
st.write("Visualizing anomalies detected by the Isolation Forest model.")

# Database Connection
def get_data():
    conn = sqlite3.connect('db/threat_hunter.db')
    # Join traffic with detected threats to see which ones are anomalies
    query = """
    SELECT t.*, d.anomaly_score, d.threat_level 
    FROM network_traffic t
    LEFT JOIN detected_threats d ON t.id = d.log_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = get_data()

# Summary Metrics
col1, col2, col3 = st.columns(3)
total_logs = len(df)
threats = df[df['threat_level'].notnull()]
col1.metric("Total Logs Analyzed", total_logs)
col2.metric("Threats Detected", len(threats))
col3.metric("System Status", "Secure" if len(threats) < 15 else "Critical")

# 3D/2D Scatter Plot
st.subheader("Traffic Analysis Map")
st.write("Red points represent anomalies isolated by the AI.")

# Mark anomalies for the chart
df['Status'] = df['threat_level'].fillna('Normal')

fig = px.scatter(df, 
                 x="packet_size", 
                 y="duration", 
                 color="Status",
                 hover_data=['source_ip', 'id'],
                 color_discrete_map={'Normal': 'blue', 'High': 'red', 'Medium': 'orange'},
                 title="Packet Size vs. Duration Outliers")

st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("Recent Threat Logs")
st.dataframe(threats[['id', 'source_ip', 'packet_size', 'duration', 'anomaly_score', 'threat_level']])

# Auto-refresh button
if st.button('Refresh Data'):
    st.rerun()