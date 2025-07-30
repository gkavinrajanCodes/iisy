from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
import numpy as np

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y , random_state=42)


clf = RandomForestClassifier(n_estimators= 50)
clf.fit(X_train, y_train)


probs = clf.predict_proba(X_test)

confidences = np.max(probs, axis = 1)
preds = np.argmax(probs, axis= 1)
correct = (preds == y_test)

bins = np.linspace(0.0,1.0,11)
binids = np.digitize(confidences, bins)-1

ece = 0.0
mce= 0.0
bin_acc = []
bin_conf = []

for i in range(len(bins)-1):
    bin_mask = binids == i
    bin_size = np.sum(bin_mask)
    if bin_size >0:
        acc = np.mean(correct[bin_mask])
        conf = np.mean(confidences[bin_mask])
        bin_acc.append(acc)
        bin_conf.append(conf)
        ece += np.abs(acc-conf) * bin_size /len(confidences)
        mce = max(mce, np.abs(acc-conf))


plt.figure(figsize=(8,6))


plt.plot([0,1], [0,1],"k:", label = "Perfectly calibrated")
plt.plot(bin_conf, bin_acc, "s-", label = "Model")
plt.xlabel("Confidence")
plt.ylabel("Accuracy")
plt.title("Reliability Diagram (Iris)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("reliability_iris.png", bbox_inches= 'tight')


print(f"ECE: {ece:.4f}, MCE: {mce:.4f}")







