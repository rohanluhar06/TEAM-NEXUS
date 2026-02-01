import instaloader
from datetime import datetime


def extract_instagram_features(username: str):
    L = instaloader.Instaloader()

    profile = instaloader.Profile.from_username(L.context, username)

    followers = profile.followers
    following = profile.followees
    posts = profile.mediacount
    bio = profile.biography or ""
    verified = int(profile.is_verified)

    # -------------------------
    # Account age + post rate
    # -------------------------
    try:
        first_post = next(profile.get_posts())
        account_age_days = (
            datetime.now(first_post.date_utc.tzinfo)
            - first_post.date_utc
        ).days
        posts_per_day = posts / max(account_age_days, 1)
    except StopIteration:
        account_age_days = 0
        posts_per_day = 0

    # -------------------------
    # Derived ML features
    # -------------------------
    ratio = followers / max(following, 1)
    username_randomness = sum(c.isdigit() for c in username) / max(len(username), 1)

    features = {
        "bio_length": len(bio),
        "username_randomness": username_randomness,
        "followers": followers,
        "following": following,
        "follower_following_ratio": ratio,
        "account_age_days": account_age_days,
        "posts_per_day": posts_per_day,
        "caption_similarity_score": 0.0,
        "content_similarity_score": 0.0,
        "spam_comments_rate": 0.0,
        "suspicious_links_in_bio": int("http" in bio.lower()),
        "verified": verified,
        "spam_keywords_count": 0
    }

    # -------------------------
    # Frontend display info
    # -------------------------
    profile_info = {
        "followers": followers,
        "following": following,
        "posts": posts,
        "account_age_days": account_age_days,
        "verified": verified
    }

    return features, profile_info
