import pandas as pd
from sklearn.ensemble import IsolationForest

class ThreatDetector:
    def __init__(self, contamination=0.05):
        # contamination is the estimated % of traffic that is malicious
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def train(self, data):
        # We only train on numerical features: packet_size and duration
        features = data[['packet_size', 'duration']]
        self.model.fit(features)

    def predict(self, data):
        features = data[['packet_size', 'duration']]
        # -1 = Anomaly, 1 = Normal
        predictions = self.model.predict(features)
        scores = self.model.decision_function(features)
        return predictions, scores