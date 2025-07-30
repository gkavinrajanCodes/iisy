import numpy as np
import pandas as pd
from scipy.stats import entropy
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


df = pd.read_csv("unsw_processed_4f.csv")
X = df.drop("label", axis=1).values
y = df['label'].values


clf = RandomForestClassifier(n_estimators= 10, random_state=42)
clf.fit(X,y)

T = 30
jitter_std = 0.05
all_preds = []


for _ in range(T):
    X_jittered = X+np.random.normal(0,jitter_std, X.shape)
    probs = clf.predict_proba(X_jittered)
    all_preds.append(probs)

all_preds = np.array(all_preds)
mean_proba = all_preds.mean(axis=0)
predicted_labels = np.argmax(mean_proba, axis = 1)
uncertainty = entropy(mean_proba.T)

acc = accuracy_score(y,predicted_labels)
print(f"Accuracy: {acc:.4f}")
print(f"Mean Predictive Entropy (uncertainty): {np.mean(uncertainty):.4f}")


plt.figure(figsize=(8,5))
plt.hist(uncertainty, bins = 30, color='#1f77b4', edgecolor='black', alpha = 0.7)
plt.axvline(np.mean(uncertainty), color='red', linestyle = 'dashed', linewidth = 1.5, label = f"Mean = {np.mean(uncertainty):.4f}")
plt.title("Predictive Entropy Distribution (Simulated MC Dropout)")
plt.xlabel("Entropy")
plt.ylabel("Number of samples")
plt.legend()
plt.grid(alpha = 0.3)
plt.tight_layout()
plt.savefig("images/mc_dropout_entropy.png")
plt.show()


