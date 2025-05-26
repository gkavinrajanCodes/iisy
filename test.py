import pickle

with open("log/switch_model_clf.pickle", "rb") as f:
    model_data = pickle.load(f)

print(model_data)
