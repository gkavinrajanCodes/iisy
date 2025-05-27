import pickle
import json
import numpy as np

def extract_tree_rules(tree):
    tree_ = tree.tree_
    rules = []

    def recurse(node, conditions):
        if tree_.feature[node] != -2:
            f = tree_.feature[node]
            t = tree_.threshold[node]
            left = tree_.children_left[node]
            right = tree_.children_right[node]

            recurse(left, conditions + [(f, "<=", t)])
            recurse(right, conditions + [(f, ">", t)])
        else:
            # Leaf node
            class_val = tree_.value[node][0]
            predicted_class = int(class_val.argmax())
            rules.append({
                "conditions": conditions,
                "class": predicted_class
            })

    recurse(0, [])
    return rules

# Load the model
with open("log/switch_model_clf.pickle", "rb") as f:
    model = pickle.load(f)

rf = model
forest_rules = []

for i, tree in enumerate(rf.estimators_):
    tree_rules = extract_tree_rules(tree)
    forest_rules.append(tree_rules)

# Create a custom JSON encoder class
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Handle numpy longlong type
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# Save to JSON
with open("log/forest_rules.json", "w") as f:
    json.dump(forest_rules, f, indent=4, cls=CustomJSONEncoder)

print("✅ Extracted rules saved to log/forest_rules.json")
