import sys
from instagram.insta_feature_extractor import extract_instagram_features
from model.predict import predict_bot_risk

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_instagram_account.py <username>")
        sys.exit(1)

    username = sys.argv[1].replace("@", "").strip()

    print(f"[+] Fetching Instagram data for @{username} ...")

    features = extract_instagram_features(username)
    result = predict_bot_risk(features)

    print("\n--- Instagram Account Risk Analysis ---")
    print(f"Username: @{username}")
    print(f"Risk Score: {result['bot_risk_score']}")
    print(f"Risk Level: {result['risk_level']}")
    print("Reasons:")
    for r in result["explanations"]:
        print("-", r)

if __name__ == "__main__":
    main()
