import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay, brier_score_loss
from sklearn.model_selection import train_test_split


with open("forest_rules_iris.json") as f:
    forest = json.load(f)

X, y = load_iris(return_X_y= True)
class_names = load_iris().target_names


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

def simulate_packet_processing(sample_features):
    votes = []
    confidences = []
    for tree in forest:
        matched = True
        for rule in tree['rules']:
            match = True
            for cond in rule['conditions']:
                feature, op, threshold = cond
                feature_idx = int(feature.split("_")[1])
                value = sample_features[feature_idx]

                if op == "<=" and not value <= threshold:
                    match = False
                elif op == ">" and not value > threshold:
                    match = True
                
            if match:
                votes.append(rule['class'])
                confidences.append(rule['confidence'])
                matched = True
                break
        if not matched:
            votes.append(-1)
            confidences.append(0.0)
    return votes, confidences

preds, all_confs = [],[]

for xi in X_test:
    votes,  confs = simulate_packet_processing(xi)
    valid = [(v,c) for v, c in zip(votes, confs) if v != -1]
    if valid:
        score = {}
        for v, c in valid:
            score[v] = score.get(v,0) + c
        pred = max(score, key=score.get)
        confidence = score[pred]/sum(score.values())
    else:
        pred = -1
        confidence = 0.0
    preds.append(pred)
    all_confs.append(confidence)

preds = np.array(preds)
mask = preds != -1
y_masked = y_test[mask]
preds_masked = preds[mask]
confs_masked =  np.array(all_confs)[mask]


plt.figure(figsize=(8,4))
plt.scatter(range(len(confs_masked)), confs_masked, c = preds_masked, cmap='tab10')
plt.title("Prediction confidence per sample")
plt.xlabel("Sample Index")
plt.ylabel("Confidence")
plt.colorbar(label = 'Predicted Class')
plt.tight_layout()
plt.savefig("images/iris_confidence_scatter.png")


plt.figure(figsize=(6,4))
plt.hist(confs_masked, bins = 10, color='skyblue', edgecolor= 'black')
plt.title("Confidence Histogram")
plt.xlabel("Confidence")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("images/iris_confidence_histogram.png")


def calibration_bins(probs, labels, preds, n_bins = 10):
    bins = np.linspace(0.0, 1.0, n_bins+1)
    ece = 0
    mce = 0
    bin_centers, accs, confs = [], [], []

    for i in range(n_bins):
        bin_mask = (probs>bins[i]) & (probs <= bins[i+1])
        bin_size = np.sum(bin_mask)
        if bin_size > 0:
            bin_acc = np.mean(preds[bin_mask] == labels[bin_mask])
            bin_conf = np.mean(probs[bin_mask])
            accs.append(bin_acc)
            confs.append(bin_conf)
            bin_centers.append((bins[i] + bins[i+1])/2)
            ece += bin_size/len(probs)*abs(bin_acc-bin_conf)
            mce += max(mce, abs(bin_acc-bin_conf))
    return ece, mce, bin_centers, accs, confs

ece, mce, bin_centers, accs, confs = calibration_bins(confs_masked, y_masked, preds_masked)

plt.figure(figsize=(6,5))
plt.plot([0,1], [0,1], 'k--', label="Perfect Calibration")
plt.plot(bin_centers, accs, 'o-', label = "Observed Accuracy")
plt.bar(bin_centers, np.abs(np.array(accs)-np.array(confs)), width=0.08, alpha = 0.2, color = 'red', label = "Gap (MCE)")
plt.xlabel("Confidence")
plt.ylabel("Accuracy")
plt.title(f"Calibration Curve\n ECE = {ece:.3f}, MCE = {mce:.3f}")
plt.legend()
plt.tight_layout()
plt.savefig("images/iris_calibration_curve.png")
plt.close()


cm = confusion_matrix(y_masked, preds_masked)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("images/iris_confusion_matrix.png")
plt.close()


report = classification_report(y_masked, preds_masked, target_names=class_names, digits=3)
with open("iris_classification_report.txt", "w") as f:
    f.write(report)

f.close()

brier = brier_score_loss(y_masked == preds_masked, confs_masked)
with open("iris_brier_score.txt", "w") as f:
    f.write(f"Brier score: {brier:.4f}")
f.close()



