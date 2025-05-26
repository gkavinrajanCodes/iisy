import pickle

# Load the switch model
with open("log/switch_model_clf.pickle", "rb") as f:
    model = pickle.load(f)

# Extract the actual scikit-learn RandomForestClassifier
rf = model  # if it's already a sklearn classifier, otherwise model.classifier or similar

# Loop through trees
for i, tree in enumerate(rf.estimators_):
    print(f"\n🌳 Tree {i}")
    tree_ = tree.tree_

    for node in range(tree_.node_count):
        if tree_.feature[node] != -2:  # -2 means it's a leaf
            print(f"Node {node}: if feature[{tree_.feature[node]}] <= {tree_.threshold[node]:.4f}")
        else:
            # Leaf node: print class prediction
            class_val = tree_.value[node][0]
            predicted_class = class_val.argmax()
            print(f"Leaf Node {node}: Predict class {predicted_class}")
