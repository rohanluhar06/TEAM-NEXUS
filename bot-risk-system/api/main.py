import sys
import os
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# ---------------------------------
# Allow importing from project root
# ---------------------------------
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ---------------------------------
# Project imports
# ---------------------------------
from model.predict import predict_bot_risk
from instagram.insta_feature_extractor import extract_instagram_features


# ---------------------------------
# FastAPI App
# ---------------------------------
app = FastAPI(
    title="Fake Account Detection API",
    description="Bot Risk Scoring and Explainability Service",
    version="1.0.0"
)
# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ===============================
# Request Schemas
# ===============================

class AccountFeatures(BaseModel):
    bio_length: Optional[int] = 0
    username_randomness: Optional[float] = 0.0
    followers: Optional[int] = 0
    following: Optional[int] = 0
    follower_following_ratio: Optional[float] = 0.0
    account_age_days: Optional[int] = 0
    posts_per_day: Optional[float] = 0.0
    caption_similarity_score: Optional[float] = 0.0
    content_similarity_score: Optional[float] = 0.0
    spam_comments_rate: Optional[float] = 0.0
    suspicious_links_in_bio: Optional[int] = 0
    verified: Optional[int] = 0
    spam_keywords_count: Optional[int] = 0


class InstagramRequest(BaseModel):
    username: str


# ===============================
# Health Check
# ===============================

@app.get("/")
def health_check():
    return {"status": "API is running"}


# ===============================
# Manual Feature Analysis Endpoint
# ===============================

@app.post("/analyze")
def analyze_account(features: AccountFeatures):
    return predict_bot_risk(features.dict())


# ===============================
# Instagram Live Analysis Endpoint
# ===============================

@app.post("/analyze-instagram")
def analyze_instagram(req: InstagramRequest):
    username = req.username.replace("@", "").strip()

    try:
        features, profile_info = extract_instagram_features(username)
    except Exception as e:
        return {
            "error": True,
            "message": "Instagram fetch failed",
            "details": str(e)
        }

    result = predict_bot_risk(features)

    return {
        "username": username,
        "profile": profile_info,      # ✅ THIS WAS MISSING
        "analysis": result
    }


