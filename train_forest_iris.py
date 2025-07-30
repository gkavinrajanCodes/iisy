import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.tree import _tree
import numpy as np

X,y = load_iris(return_X_y=True)
clf = RandomForestClassifier(n_estimators=3, max_depth=2, random_state=42)
clf.fit(X,y)

forest_rules = []
for idx, estimator in enumerate(clf.estimators_):
    tree = estimator.tree_
    rules = []

    def extract_rule(node, conditions):
        if tree.feature[node] != _tree.TREE_UNDEFINED:
            name = f"feature_{tree.feature[node]}"
            thresh = tree.threshold[node]
            extract_rule(tree.children_left[node], conditions + [(name, "<=", thresh)])
            extract_rule(tree.children_right[node], conditions + [(name, ">", thresh)])
        else:
            prob = tree.value[node][0]/np.sum(tree.value[node][0])
            prediction = int(np.argmax(tree.value[node][0]))
            confidence = float(np.max(prob))
            rules.append(
                {
                    "conditions": conditions,
                    "class": prediction,
                    "confidence": confidence
                }
            )
    extract_rule(0, [])
    forest_rules.append({"tree_id": idx, "rules": rules})

with open("forest_rules_iris.json", "w") as f:
    json.dump(forest_rules, f, indent=2)

print("Extracted rules from Random forest and saved to forest_rules_iris.json")









