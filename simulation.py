import time
import random
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import logging

X = np.array([[100], [200], [300], [400]])
y = np.array([1,1,0,0])

clf = DecisionTreeClassifier(max_depth=2)
clf.fit(X,y)


logging.basicConfig(level=logging.INFO)

def send_packet_simulated(port_value):
    logging.info(f"\n Packet send with feature_1 = {port_value}")
    return {'feature_1':port_value}

def p4_classifier(packet):
    port = packet['feature_1']
    if port <=248:
        confidence = 'high'
        predicted_class = 1
    else:
        confidence = 'low'
        predicted_class = None
    return confidence, predicted_class


def run_ml_model(packet):
    features = [packet['feature_1']]
    pred = clf.predict([features])[0]

    return pred

def simulation_pipeline(port_value):
    packet = send_packet_simulated(port_value)

    start_time = time.perf_counter()
    confidence, predicted_class = p4_classifier(packet)
    p4_time = time.perf_counter() - start_time

    if confidence == 'high':
        logging.info(f"Classified in P4 with HIGH confidence: class = {predicted_class}")
        logging.info(f"Latency (P4-only path): {p4_time*1000:.3f} ms")
    else:
        logging.info("Low confidence in P4 -> offloading to Python ML...")
        start_time - time.perf_counter()
        predicted_class = run_ml_model(packet)
        host_time = time.perf_counter() - start_time
        logging.info(f"Final prediction from Python ML class = {predicted_class}")
        logging.info(f"Latency (host ML path): {host_time*1000:.3f} ms")




simulation_pipeline(200)
simulation_pipeline(300)