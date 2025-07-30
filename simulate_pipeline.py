import json
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


with open("forest_rules_iris.json") as f:
    forest = json.load(f)

X, y = load_iris(return_X_y=True)
feature_names = [f"feature{i}" for i in range(X.shape[1])]

def simulate_packet_processing(sample_features):
    votes = []
    confidences = []

    for tree in forest:
        matched = False
        for rule in tree['rules']:
            match = True
            for cond in rule['conditions']:
                feature, op, threshold = cond
                feature_idx = int(feature.split("_")[1])
                value = sample_features[feature_idx]
                if op == "<=" and not value <= threshold:
                    match = False
                elif op == ">" and not value > threshold:
                    match = False
            if match:
                votes.append(rule["class"])
                confidences.append(rule["confidence"])
                matched = True
                break
        if not matched:
            votes.append(-1)
            confidences.append(0.0)
    return votes, confidences



preds = []
true_confidences = []

for xi in X:
    votes, confs = simulate_packet_processing(xi)
    valid_votes = [(v, c) for v,c in zip(votes, confs) if v!= -1]
    if valid_votes:
        class_scores = {}
        for v, c in valid_votes:
            class_scores[v] = class_scores.get(v,0) +c
        pred = max(class_scores, key= class_scores.get)
        confidence = class_scores[pred]/sum(class_scores.values())

    else:
        pred = -1
        confidence = 0.0
    preds.append(pred)
    true_confidences.append(confidence)


preds = np.array(preds)
mask = preds != -1
y_masked = np.array([yi for pi, yi in zip(preds, y) if pi != -1])
preds_masked = preds[mask]
confidences_masked = np.array([ci for pi, ci in zip(preds, true_confidences) if pi != -1])



plt.figure(figsize= (8,5))
plt.scatter(range(len(confidences_masked)), confidences_masked, c = preds_masked, cmap="tab10")
plt.title("Prediction confidence per sample")
plt.xlabel("Sample index")
plt.ylabel("Confidence")
plt.colorbar(label = "Predicted class")
plt.tight_layout()
plt.savefig("confidence_scatter.png")
plt.close()


plt.figure(figsize=(6,4))
plt.hist(confidences_masked, bins = 10, color = "steelblue", edgecolor = "black")
plt.title("Confidence Histogram")
plt.xlabel("Confidence")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("confidence_histogram.png")
plt.close()


def calibration_bins(probs, labels, n_bins = 10):
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0
    mce = 0
    bin_centers = []
    accs = []
    confs = []

    for i in range(n_bins):
        bin_mask = (probs > bins[i]) & (probs <= bins[i+1])
        bin_size = np.sum(bin_mask)

        if bin_size > 0:
            bin_acc = np.mean(preds_masked[bin_mask] == y_masked[bin_mask])
            bin_conf = np.mean(probs[bin_mask])
            accs.append(bin_acc)
            confs.append(bin_conf)
            bin_centers.append((bins[i]+bins[i+1])/2)
            ece += bin_size/len(probs) * abs(bin_acc-bin_conf)

            mce = max(mce, abs(bin_acc-bin_conf))

    return ece, mce, bin_centers, accs, confs


ece, mce, bin_centers, accs, confs = calibration_bins(confidences_masked, y_masked)

plt.figure(figsize=(6,5))
plt.plot([0,1], [0,1], 'k--', label = "Perfect Cailbration")
plt.plot(bin_centers, accs, 'o-', label = "Observed Accuracy")
plt.bar(bin_centers, np.abs(np.array(accs)-np.array(confs)), width=0.08, alpha = 0.2, color = 'red', label = "Gap(MCE)")
plt.xlabel("Confidence")
plt.ylabel("Accuracy")
plt.title(f"Calibration Curve\n ECE={ece:.3f}, MCE={mce:.3f}")
plt.legend()
plt.tight_layout()
plt.savefig("calibration_curve.png")
plt.close()


print("---------------------SIMULATION COMPLETE----------------------")
print(f"Accuracy: {accuracy_score(y_masked, preds_masked)* 100:.2f}")
print(f"ECE: {ece:.3f}, MCE: {mce:.3f}")
print("Plots saved")
