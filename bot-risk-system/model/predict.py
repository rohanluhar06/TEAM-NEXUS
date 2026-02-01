import sys
import os
import joblib
import pandas as pd

sys.path.append(os.path.dirname(__file__))

from rules import apply_rule_based_scoring

# ---------------------------------------
# Load trained ML model
# ---------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "bot_risk_model.pkl")
model = joblib.load(MODEL_PATH)

# ML features used during training (MUST match train_model.py)
ML_FEATURES = [
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


def predict_bot_risk(account_features: dict):
    """
    Predicts bot risk score for a single account.
    """

    # -------------------------------
    # 1. Prepare ML input (FILTERED)
    # -------------------------------
    ml_input = {k: account_features.get(k, 0) for k in ML_FEATURES}
    df = pd.DataFrame([ml_input]).fillna(0)

    # -------------------------------
    # 2. ML Probability Prediction
    # -------------------------------
    fake_probability = model.predict_proba(df)[0][1]
    ml_score = fake_probability * 100

    # -------------------------------
    # 3. Rule-Based Scoring (FULL FEATURES)
    # -------------------------------
    rule_score, rule_reasons = apply_rule_based_scoring(account_features)

    # -------------------------------
    # 4. Final Score Combination
    # -------------------------------
    final_score = round((0.7 * ml_score) + (0.3 * rule_score), 2)

    # -------------------------------
    # 5. Risk Level
    # -------------------------------
    if final_score < 40:
        risk_level = "LOW"
    elif final_score < 70:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    # -------------------------------
    # 6. Output
    # -------------------------------
    return {
    "bot_risk_score": float(final_score),
    "risk_level": risk_level,
    "ml_probability": float(round(fake_probability, 3)),
    "rule_score": int(rule_score),
    "explanations": rule_reasons
}



# -------- TEMP TEST (REMOVE LATER) --------
if __name__ == "__main__":
    sample_account = {
        "bio_length": 5,
        "username_randomness": 0.9,
        "followers": 40,
        "following": 900,
        "follower_following_ratio": 0.04,
        "account_age_days": 10,
        "posts_per_day": 15,
        "caption_similarity_score": 0.85,
        "content_similarity_score": 0.9,
        "spam_comments_rate": 0.7,
        "suspicious_links_in_bio": 1,
        "verified": 0,
        "spam_keywords_count": 5
    }

    print(predict_bot_risk(sample_account))
