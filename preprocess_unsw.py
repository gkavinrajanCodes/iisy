import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, mutual_info_classif

print("Loading UNSW - NB15 dataset...")
df = pd.read_csv("dataset/UNSW_NB15_training-set.csv")

df.drop(columns=["id", "label", "attack_cat"], errors = 'ignore', inplace = True)

cat_cols = df.select_dtypes(include = ["object"]).columns
for col in cat_cols:
    df[col] = LabelEncoder().fit_transform(df[col])


X = df.drop("label", axis=1 , errors = 'ignore')
y = pd.read_csv("dataset/UNSW_NB15_training-set.csv")['label']

scaler = MinMaxScaler()
X_scaled= scaler.fit_transform(X)


selector_4 = SelectKBest(mutual_info_classif, k = 4)
X_4f = selector_4.fit_transform(X_scaled, y)
selected_4f = selector_4.get_support(indices=True)


selector_6 = SelectKBest(mutual_info_classif, k = 6)
X_6f = selector_6.fit_transform(X_scaled, y)
selected_6f = selector_6.get_support(indices=True)

X_4f_df = pd.DataFrame(X_4f, columns=[X.columns[i] for i in selected_4f])
X_6f_df = pd.DataFrame(X_6f, columns=[X.columns[i] for i in selected_6f])

X_4f_df['label'] = y
X_6f_df['label'] = y

X_4f_df.to_csv("unsw_processed_4f.csv", index = True)
X_6f_df.to_csv("unsw_processed_6f.csv", index = True)

print("Saved the files....")








