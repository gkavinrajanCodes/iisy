# === uncertainty_unsw_metrics.py ===
import json
import numpy as np
import pandas as pd
from scipy.stats import entropy
from sklearn.preprocessing import MinMaxScaler

# Load rules
with open("forest_rules_unsw.json") as f:
    forest = json.load(f)

# Load UNSW dataset
df = pd.read_csv("unsw_processed_4f.csv")
X = df.drop("label", axis=1).values
y = df["label"].values

# === PAC: Agreement-based Confidence ===
def simulate_pac(xi):
    votes = []
    confs = []
    for tree in forest:
        matched = False
        for rule in tree["rules"]:
            match = True
            for cond in rule["conditions"]:
                feat, op, thresh = cond
                idx = int(feat.split("_")[1])
                val = xi[idx]
                if op == "<=" and not val <= thresh:
                    match = False
                if op == ">" and not val > thresh:
                    match = False
            if match:
                votes.append(rule["class"])
                confs.append(rule["confidence"])
                matched = True
                break
        if not matched:
            votes.append(-1)
            confs.append(0.0)

    vote_counts = {}
    for v in votes:
        if v != -1:
            vote_counts[v] = vote_counts.get(v, 0) + 1

    if len(vote_counts) == 0:
        return 0.0, 0.0, 0.0

    total = sum(vote_counts.values())
    max_agreement = max(vote_counts.values())
    agreement = max_agreement / total
    prob_dist = np.array(list(vote_counts.values())) / total
    pe_calib = entropy(prob_dist)  # PEC
    return agreement, pe_calib, votes

# === DBC: Distance to Decision Boundary (Approximate)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

def compute_dbc(xi, rule_set):
    distances = []
    for tree in rule_set:
        for rule in tree["rules"]:
            d = 0
            for cond in rule["conditions"]:
                feat, op, thresh = cond
                idx = int(feat.split("_")[1])
                val = xi[idx]
                if op == "<=" and val > thresh:
                    d += abs(val - thresh)
                elif op == ">" and val <= thresh:
                    d += abs(thresh - val)
            distances.append(d)
    return min(distances)

# === Run on all samples ===
agreements, pecs, dbcs = [], [], []
for xi in X_scaled:
    agreement, pec, _ = simulate_pac(xi)
    dbc = compute_dbc(xi, forest)
    agreements.append(agreement)
    pecs.append(pec)
    dbcs.append(dbc)

# Normalize DBC for plotting
dbcs = np.array(dbcs)
dbcs_scaled = (dbcs - dbcs.min()) / (dbcs.max() - dbcs.min())

# === Save scatter plots ===
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.scatter(range(len(agreements)), agreements, s=10, label="PAC", alpha=0.7)
plt.scatter(range(len(pecs)), pecs, s=10, label="PEC", alpha=0.7)
plt.scatter(range(len(dbcs_scaled)), dbcs_scaled, s=10, label="DBC (norm)", alpha=0.7)
plt.title("Uncertainty Estimation on UNSW-NB15")
plt.xlabel("Sample Index")
plt.ylabel("Uncertainty Metrics")
plt.legend()
plt.tight_layout()
plt.savefig("images/unsw_uncertainty_metrics.png")
plt.close()

print("Saved unsw_uncertainty_metrics.png ✅")
