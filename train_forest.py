import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.tree import _tree
import numpy as np

X,y = make_classification(n_samples=100, n_features=2, n_classes=2, n_informative=2, n_redundant=0, n_repeated=0, random_state=42)
clf = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=42)
clf.fit(X,y)

rules = []
for tree_idx, estimator in enumerate(clf.estimators_):
    tree = estimator.tree_
    feature_names = [f"feature_{i}" for i in range(X.shape[1])]

    def extract_rule(node_id = 0, conditions = []):
        if tree.feature[node_id] != _tree.TREE_UNDEFINED:
            feat = feature_names[tree.feature[node_id]]
            thresh = tree.threshold[node_id]
            extract_rule(tree.children_left[node_id], conditions + [(feat, "<=", thresh)])
            extract_rule(tree.children_right[node_id], conditions + [(feat, ">", thresh)])
        else:
            prob = tree.value[node_id][0]/tree.value[node_id][0].sum()
            class_label = int(prob.argmax())
            confidence = float(prob[class_label])
            rules.append(
                {
                    "tree":tree_idx,
                    "conditions": conditions,
                    "class": class_label,
                    "confidence": confidence
                }
            )
    extract_rule()

with open("forest_rules_1.json", "w") as f:
    json.dump(rules, f, indent=2)

print("Extracted rules from Random forest and saved to forest_rules_1.json")









