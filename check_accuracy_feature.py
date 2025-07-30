import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt


print("Loading dataset")
df = pd.read_csv("dataset/UNSW_NB15_training-set.csv")


cols_to_drop = ['id', 'label', 'attack_cat', 'proto',  'service', 'state']
df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

df = df.dropna(axis = 1, how='all')
df = df.select_dtypes(include=[np.number])

X = df.drop(columns=['label']) if 'label' in df.columns else df.iloc[:, :-1]
y = df['label'] if 'label' in df.columns else df.iloc[:, -1]

if y.dtype == object:
    y = LabelEncoder().fit_transform(y)


clf = RandomForestClassifier(n_estimators=100,  random_state=42)
clf.fit(X,y)
importances = clf.feature_importances_
feature_ranking = np.argsort(importances)[::-1]
k_values = list(range(2,21,2))
accuracies = []

for k in k_values:
    top_k_indices = feature_ranking[::k]
    top_k_features = X.columns[top_k_indices]
    X_k = X[top_k_features]
    scores= cross_val_score(clf, X_k, y, cv = 5, scoring="accuracy")
    accuracies.append(np.mean(scores))
    print(f"Top {k} features: Accuracy = {np.mean(scores):.4f}")

plt.figure(figsize=(8,5))
plt.plot(k_values, accuracies, marker = 'o')
plt.title("Accuracy vs Number of Top features")
plt.xlabel("Number of features")
plt.ylabel("Cross-validated accuracy")
plt.grid(True)
plt.tight_layout()
plt.savefig("accuracy_vs_feature.png")
plt.close()

top_features = X.columns[feature_ranking[:20]].to_list()

with open("top_20_features.txt", "w") as f:
    for rank, name in enumerate(top_features):
        f.write(f"{rank +1}. {name}\n")

print("Process done")




