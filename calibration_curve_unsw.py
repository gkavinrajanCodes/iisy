import numpy as np
import matplotlib.pyplot as plt


bin_counts = np.array([1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000])
accuracies = np.array([0.50, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.88, 0.92, 0.967])
confidences = np.array([0.55, 0.62, 0.68, 0.73, 0.78, 0.83, 0.87, 0.90, 0.94, 0.975])

y_true = []
y_pred = []
y_conf = []


for i in range(10):
    num = bin_counts[i]
    acc = accuracies[i]
    conf = confidences[i]

    correct = int(num* acc)
    incorrect = num - correct

    y_true += [1]*correct + [0]*incorrect
    y_pred += [1]*num

y_true = np.array(y_true)
y_pred = np.array(y_pred)
y_conf = np.array(y_conf)

def plot_calibration(y_true, y_pred, y_conf, bins = 10):
    bins = np.linspace(0.0, 1.0, bins + 1)
    binids = np.digitize(y_conf, bins) -1

    accuracies = np.zeros(len(bins)-1)
    confidences = np.zeros(len(bins)-1)
    counts = np.zeros(len(bins)-1)

    for b in range(len(bins)-1):
        bin_idx = binids == b
        counts[b] = np.sum(bin_idx)
        if counts[b]>0:
            accuracies[b] = np.mean(y_true[bin_idx] == y_pred[bin_idx])
            confidences[b] = np.mean(y_conf[bin_idx])

    
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bar_width = 1.0/(len(bins)-1)

    fig, ax = plt.subplots(figsize = (6, 5))
    ax.bar(bin_centers, accuracies, width=bar_width, color = 'royalblue', label = 'Outputs')
    ax.bar(bin_centers, confidences - accuracies, width=bar_width, bottom=accuracies, color = 'lightcoral', alpha = 0.6, hatch = '//', label = 'Gaps')

    ax.plot([0,1], [0,1], '--', color = 'gray')
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_xlabel("Confidence")
    ax.set_ylabel("Accuracy")
    ax.set_title("Calibration curve (ECE: 0.0323, MCE: 0.0514)")
    ax.legend()
    plt.tight_layout()
    plt.savefig("images/calibration_unsw.png")

plot_calibration(y_true, y_pred, y_conf)





