# === simulate_unsw_classification.py ===
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, brier_score_loss

# Load extracted rules
with open("forest_rules_unsw.json") as f:
    forest = json.load(f)

# Load the 4-feature UNSW-NB15 dataset
df = pd.read_csv("unsw_processed_4f.csv")
X = df.drop("label", axis=1).values
y = df["label"].values

# Packet-based simulation of classification
def simulate_packet(features):
    votes = []
    confs = []
    for tree in forest:
        matched = False
        for rule in tree["rules"]:
            match = True
            for cond in rule["conditions"]:
                feat, op, threshold = cond
                idx = int(feat.split("_")[1])
                value = features[idx]
                if op == "<=" and not value <= threshold:
                    match = False
                elif op == ">" and not value > threshold:
                    match = False
            if match:
                votes.append(rule["class"])
                confs.append(rule["confidence"])
                matched = True
                break
        if not matched:
            votes.append(-1)
            confs.append(0.0)
    return votes, confs

preds, all_confs = [], []
for xi in X:
    votes, confs = simulate_packet(xi)
    valid = [(v, c) for v, c in zip(votes, confs) if v != -1]
    if valid:
        score = {}
        for v, c in valid:
            score[v] = score.get(v, 0) + c
        pred = max(score, key=score.get)
        confidence = score[pred] / sum(score.values())
    else:
        pred = -1
        confidence = 0.0
    preds.append(pred)
    all_confs.append(confidence)

preds = np.array(preds)
mask = preds != -1
y_masked = y[mask]
preds_masked = preds[mask]
confs_masked = np.array(all_confs)[mask]

# === Confidence Scatter Plot ===
plt.figure(figsize=(8, 4))
plt.scatter(range(len(confs_masked)), confs_masked, c=preds_masked, cmap='tab10', s=12)
plt.title("Prediction Confidence per Sample (UNSW)")
plt.xlabel("Sample Index")
plt.ylabel("Confidence")
plt.colorbar(label="Predicted Class")
plt.tight_layout()
plt.savefig("images/unsw_confidence_scatter.png")
plt.close()

# === Histogram of Confidences ===
plt.figure(figsize=(6, 4))
plt.hist(confs_masked, bins=10, color='skyblue', edgecolor='black')
plt.title("Confidence Histogram (UNSW)")
plt.xlabel("Confidence")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/unsw_confidence_histogram.png")
plt.close()

# === Calibration Curve (ECE/MCE) ===
def calibration_bins(probs, labels, n_bins=10):
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0
    mce = 0
    bin_centers = []
    accs = []
    confs = []

    for i in range(n_bins):
        mask = (probs > bins[i]) & (probs <= bins[i + 1])
        size = np.sum(mask)
        if size > 0:
            bin_acc = np.mean(preds_masked[mask] == y_masked[mask])
            bin_conf = np.mean(probs[mask])
            accs.append(bin_acc)
            confs.append(bin_conf)
            bin_centers.append((bins[i] + bins[i + 1]) / 2)
            ece += size / len(probs) * abs(bin_acc - bin_conf)
            mce = max(mce, abs(bin_acc - bin_conf))

    return ece, mce, bin_centers, accs, confs

ece, mce, bin_centers, accs, confs = calibration_bins(confs_masked, y_masked)

plt.figure(figsize=(6, 5))
plt.plot([0, 1], [0, 1], 'k--', label="Perfect Calibration")
plt.plot(bin_centers, accs, 'o-', label="Observed Accuracy")
plt.bar(bin_centers, np.abs(np.array(accs) - np.array(confs)), width=0.08, alpha=0.3, color='red', label="Gap (MCE)")
plt.xlabel("Confidence")
plt.ylabel("Accuracy")
plt.title(f"UNSW Calibration Curve\nECE = {ece:.3f}, MCE = {mce:.3f}")
plt.legend()
plt.tight_layout()
plt.savefig("images/unsw_calibration_curve.png")
plt.close()

# === Final Report ===
print("=== UNSW Simulation Complete ✅ ===")
print(f"Accuracy: {accuracy_score(y_masked, preds_masked) * 100:.2f}%")
print(f"Brier Score: {brier_score_loss(y_masked, confs_masked):.4f}")
print(f"ECE: {ece:.4f}, MCE: {mce:.4f}")
print("Saved Plots:")
print(" - unsw_confidence_scatter.png")
print(" - unsw_confidence_histogram.png")
print(" - unsw_calibration_curve.png")
