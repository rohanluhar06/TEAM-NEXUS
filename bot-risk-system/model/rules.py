def apply_rule_based_scoring(features: dict):
    """
    Applies rule-based risk scoring.
    Input: features (dict)
    Output: rule_score (0–100), triggered_rules (list)
    """

    score = 0
    triggered_rules = []

    # -------------------------------
    # Behavioural Rules
    # -------------------------------
    if features.get("posts_per_day", 0) > 10:
        score += 20
        triggered_rules.append("High posting frequency (>10 posts/day)")

    # -------------------------------
    # Network Rules
    # -------------------------------
    if features.get("following", 0) > 500:
        score += 15
        triggered_rules.append("Aggressive following (>500 accounts)")

    if (
        features.get("following", 0) > 500
        and features.get("follower_following_ratio", 1) < 0.2
    ):
        score += 30
        triggered_rules.append("Low follower-following ratio with high following")

    if (
        features.get("following", 0) > 1000
        and features.get("followers", 0) < 100
    ):
        score += 40
        triggered_rules.append("Extreme follower-following imbalance")

    # -------------------------------
    # Content Rules
    # -------------------------------
    if features.get("caption_similarity_score", 0) > 0.8:
        score += 25
        triggered_rules.append("Highly repetitive captions")

    if features.get("spam_keywords_count", 0) > 3:
        score += 30
        triggered_rules.append("High spam keyword usage")

    # -------------------------------
    # Metadata Rules
    # -------------------------------
    if features.get("username_randomness", 0) > 0.7:
        score += 25
        triggered_rules.append("Random or auto-generated username")

    if features.get("bio_length", 0) < 10 and features.get("verified", 0) == 0:
        score += 15
        triggered_rules.append("Incomplete or empty profile bio")

    if features.get("suspicious_links_in_bio", 0) == 1:
        score += 30
        triggered_rules.append("Suspicious links found in bio")

    # -------------------------------
    # Cap score to 100
    # -------------------------------
    rule_score = min(score, 100)

    return rule_score, triggered_rules


