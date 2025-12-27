import os
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load data
df = pd.read_csv("data/raw/train.csv")

# Keep numeric features only
df = df.select_dtypes(include=["int64", "float64"])

# Target
y = df["is_claim"]
X = df.drop("is_claim", axis=1)

# Calculate scale_pos_weight
neg, pos = (y == 0).sum(), (y == 1).sum()
scale_pos_weight = neg / pos

# Pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        random_state=42
    ))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline.fit(X_train, y_train)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(pipeline, "models/model.pkl")

print("✅ Model trained successfully")
