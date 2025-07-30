# === train_forest_unsw.py ===
# Train a Random Forest on UNSW-NB15 dataset (20 features) and save extracted rules as JSON

import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import _tree
from sklearn.model_selection import train_test_split

# Load full-feature dataset
DATA_PATH = "unsw_processed_6f.csv"
df = pd.read_csv(DATA_PATH)

X = df.drop("label", axis=1).values
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a deeper Random Forest with more estimators for richer rule generation
clf = RandomForestClassifier(n_estimators=10, max_depth=None, random_state=42)
clf.fit(X_train, y_train)

forest_rules = []

for idx, estimator in enumerate(clf.estimators_):
    tree = estimator.tree_
    rules = []

    def recurse(node, conditions):
        if tree.feature[node] != _tree.TREE_UNDEFINED:
            name = f"feature_{tree.feature[node]}"
            threshold = tree.threshold[node]
            recurse(tree.children_left[node], conditions + [(name, "<=", threshold)])
            recurse(tree.children_right[node], conditions + [(name, ">", threshold)])
        else:
            print("Tree value: ", tree.value)
            prob = tree.value[node][0] / np.sum(tree.value[node][0])
            prediction = int(np.argmax(tree.value[node][0]))
            rules.append({
                "conditions": conditions,
                "class": prediction,
                "confidence": float(np.max(prob))
            })

    recurse(0, [])
    forest_rules.append({"tree_id": idx, "rules": rules})

# Save to JSON
with open("forest_rules_unsw_6.json", "w") as f:
    json.dump(forest_rules, f, indent=2)

print("Saved forest_rules_unsw.json with 20-feature forest")
