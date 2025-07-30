import time
import logging
import random
import numpy as np
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig(level=logging.INFO, format='%(message)s')

np.random.seed(42)
X = np.random.randint(0,500,size = (50,2))
y = np.array([1 if x[0]<= 248 else 0 for x in X])

dt_model = DecisionTreeClassifier(max_depth=3, random_state=0)
dt_model.fit(X,y)



rf_model = RandomForestClassifier(n_estimators=5, max_depth=5, random_state=0)
rf_model.fit(X,y)



def generate_packet():
    src_port = random.randint(0,500)
    dst_port = random.randint(0,500)
    return {'src_port': src_port, 'dst_port': dst_port}

def p4_classifier(packet):
    port = packet['src_port']
    if port <= 248:
        confidence = 'high'
        predicted_class = 1
    else:
        confidence = 'low'
        predicted_class = 0
    return confidence, predicted_class


def host_ml_inference(packet):
    features = [packet['src_port'], packet['dst_port']]
    return rf_model.predict([features])[0]


N = 30
p4_latencies=  []
host_latencies = []
path_taken = []
results = []


for _ in range(N):
    packet = generate_packet()
    confidence, predicted_class = p4_classifier(packet)

    if confidence == 'high':
        start = time.perf_counter()
        time.sleep(0.0002)
        latency = time.perf_counter() - start
        p4_latencies.append(latency)
        path_taken.append("P4")
        results.append((packet,1,latency))
    else:
        start = time.perf_counter()
        predicted_class = host_ml_inference(packet)
        latency = time.perf_counter() - start
        host_latencies.append(latency)
        results.append((packet, predicted_class, latency))



plt.figure(figsize=(10,5))
plt.plot(p4_latencies, label = "P4 Path latency", marker = 'o')
plt.plot(host_latencies, label = "Host ML latency", marker = 'x')
plt.title("Latency comparison: P4 vs Host ML inference")
plt.xlabel("Packet index")
plt.ylabel("Latency (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("pipeline_latency.png")

print(f"\nTotal packets : {N}")
print(f"Classified in P4: {path_taken.count('P4')}")
print(f"Offloaded to Host ML: {path_taken.count('Host')}")

