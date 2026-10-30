import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

df = pd.read_csv(r"C:\Users\ASUS\Documents\modelJD_V4\data\เก็บข้อมูล.csv")
df_clean = df.dropna(subset=["Title", "CurriculumRoleID", "Skills"]).copy()
print(f"Dataset clean count: {len(df_clean)}")

X = df_clean["Skills"].astype(str)
y = df_clean["CurriculumRoleID"].astype(str).str.strip()

print("Class distribution:")
print(y.value_counts())

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        token_pattern=r'(?u)[a-zA-Z0-9_+#.-]+',
        ngram_range=(1, 1),
        max_features=1000
    )),
    ('clf', LogisticRegression(
        max_iter=1000,
        random_state=42,
        C=0.5
    ))
])

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
accuracies, precisions, recalls, f1s = [], [], [], []

for fold, (train_idx, test_idx) in enumerate(skf.split(X, y), 1):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    accuracies.append(accuracy_score(y_test, y_pred))
    precisions.append(precision_score(y_test, y_pred, average='macro', zero_division=0))
    recalls.append(recall_score(y_test, y_pred, average='macro', zero_division=0))
    f1s.append(f1_score(y_test, y_pred, average='macro', zero_division=0))

print("\n--- 5-Fold Stratified CV on REAL 115 Thai Jobs ---")
print(f"Accuracy : {np.mean(accuracies)*100:.2f}% (+/- {np.std(accuracies)*100:.2f}%)")
print(f"Precision: {np.mean(precisions)*100:.2f}%")
print(f"Recall   : {np.mean(recalls)*100:.2f}%")
print(f"F1-Score : {np.mean(f1s)*100:.2f}%")
