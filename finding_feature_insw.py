import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


df = pd.read_csv("dataset/UNSW_NB15_training-set.csv")
df = df.dropna(axis = 1, how='all')
df = df.select_dtypes(include=[np.number])

X = df.drop(columns=['label']) if 'label' in df.columns else df.iloc[:, :-1]
y = df['label'] if 'label' in df.columns else df.iloc[:, -1]

if y.dtype == object:
    y = LabelEncoder().fit_transform(y)


max_features = min(20, X.shape[1])
mean_accuracies = []


for k in range(1, max_features + 1):
    pipe = Pipeline([
        ("impute", SimpleImputer(strategy="mean")),
        ("scale", StandardScaler()),
        ("select", SelectKBest(score_func=f_classif, k = k)),
        ("clf", RandomForestClassifier(n_estimators=50, random_state=42))
    ])
    scores = cross_val_score(pipe, X, y, cv = 5, scoring = "accuracy")
    mean_accuracies.append(scores.mean())


plt.figure(figsize=(8,6))
plt.plot(range(1, max_features+1), mean_accuracies, marker = 'o', color = 'blue')
plt.title("Accuracy vs Number of Top features (UNSW-NB15)")
plt.xlabel("Number of features")
plt.ylabel("Cross validated accuracy")
plt.grid(True)
plt.tight_layout()
plt.savefig("accuracy_vs_feature_count.png")
plt.show()




