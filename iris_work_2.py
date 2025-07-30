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
bin_sizes = []


for i in range(len(bins)-1):
    bin_mask = binids == i
    bin_size = np.sum(bin_mask)
    if bin_size >0:
        acc = np.mean(correct[bin_mask])
        conf = np.mean(confidences[bin_mask])
        bin_acc.append(acc)
        bin_conf.append(conf)
        bin_sizes.append(bin_size)
        ece += np.abs(acc-conf) * bin_size /len(confidences)
        mce = max(mce, np.abs(acc-conf))
    else:
        bin_acc.append(0)
        bin_conf.append(0)
        bin_sizes.append(0)


fig, (ax1, ax2) = plt.subplots(2,1, figsize = (8, 8), sharex=True, gridspec_kw={'height_ratios': [3,1]})

ax1.plot([0,1], [0,1], "k:", label = "Perfectly calibrated")
ax1.plot(bin_conf, bin_acc, "s-", label = "Model")
ax1.set_ylabel("Accuracy")
ax1.set_title("Reliability diagram + Confidence Histogram (Iris)")
ax1.legend()
ax1.grid(True)

ax2.bar(bins[:-1], bin_sizes, width = 0.1, align = 'edge',  edgecolor = 'black')
ax2.set_xlabel("Confidence")
ax2.set_ylabel("Frequency")
ax2.grid(True)



plt.tight_layout()
plt.savefig("reliability_histogram_iris.png", bbox_inches = 'tight')
print(f"ECE: {ece:.4f}")
print(f"MCE: {mce:.4f}")


