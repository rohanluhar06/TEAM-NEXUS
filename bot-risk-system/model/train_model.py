import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------
DATA_PATH = "../data/fake_social_media.csv"

data = pd.read_csv(DATA_PATH)
print("Dataset loaded successfully")
print("Shape:", data.shape)

# --------------------------------------------------
# 2. Define features and target
# --------------------------------------------------
FEATURES = [
    "bio_length",
    "username_randomness",
    "followers",
    "following",
    "follower_following_ratio",
    "account_age_days",
    "posts_per_day",
    "caption_similarity_score",
    "content_similarity_score",
    "spam_comments_rate",
    "suspicious_links_in_bio",
    "verified"
]

TARGET = "is_fake"

X = data[FEATURES]
y = data[TARGET]

# --------------------------------------------------
# 3. Handle missing values
# --------------------------------------------------
X = X.fillna(0)

# --------------------------------------------------
# 4. Train-test split
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------------------------
# 5. Train the model
# --------------------------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# --------------------------------------------------
# 6. Evaluate the model
# --------------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%\n")
print("Classification Report:\n")
print(classification_report(y_test, y_pred))

# --------------------------------------------------
# 7. Save trained model
# --------------------------------------------------
MODEL_PATH = "bot_risk_model.pkl"
joblib.dump(model, MODEL_PATH)

print(f"\n✅ Model saved as {MODEL_PATH}")
