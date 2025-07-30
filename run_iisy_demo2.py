# Retry after correcting calibration_curve import
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, brier_score_loss
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.calibration import calibration_curve

# Load preprocessed UNSW-NB15 dataset (4 features)
df = pd.read_csv("unsw_processed_4f.csv")
X = df.drop("label", axis=1).values
y = df["label"].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Random Forest
clf = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# Accuracy vs Feature Count
feature_counts = list(range(1, 21))
accuracies = []
df_full = pd.read_csv("unsw_processed_6f.csv")
X_full = df_full.drop("label", axis=1)
y_full = df_full["label"]

for n in feature_counts:
    acc = cross_val_score(RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42),
                          X_full.iloc[:, :n], y_full, cv=3).mean()
    accuracies.append(acc)

# Plot 1: Accuracy vs Feature Count
plt.figure(figsize=(8, 5))
plt.plot(feature_counts, accuracies, marker='o', color='teal')
plt.title("Accuracy vs Feature Count (UNSW-NB15)")
plt.xlabel("Number of Features")
plt.ylabel("Cross-Validation Accuracy")
plt.grid(True)
plt.tight_layout()
plt.savefig("images/accuracy_vs_features_unsw.png")

# Predict and Confusion Matrix
y_pred = clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap='Blues')
plt.title("Confusion Matrix (UNSW-NB15 - IIsy)")
plt.tight_layout()
plt.savefig("images/confusion_matrix_unsw.png")

# Calibration Curve and Brier Score
y_prob = clf.predict_proba(X_test)
confidences = np.max(y_prob, axis=1)
true_confidences = (y_pred == y_test).astype(int)

prob_true, prob_pred = calibration_curve(true_confidences, confidences, n_bins=10)

# Plot 2: Calibration Curve
plt.figure(figsize=(6, 5))
plt.plot(prob_pred, prob_true, marker='o', label='IIsy Model')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectly Calibrated')
plt.title("Calibration Curve (UNSW-NB15)")
plt.xlabel("Mean Predicted Confidence")
plt.ylabel("True Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("images/calibration_curve_unsw.png")

# Plot 3: Confidence Histogram
plt.figure(figsize=(6, 5))
sns.histplot(confidences, bins=10, kde=False, color="purple")
plt.title("Prediction Confidence Distribution (UNSW-NB15)")
plt.xlabel("Confidence")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("images/confidence_histogram_unsw.png")

# Brier Score
brier = brier_score_loss(true_confidences, confidences)
print(brier)
