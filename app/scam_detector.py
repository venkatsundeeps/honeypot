def detect_scam(message: str):
    keywords = [
        "blocked", "verify", "urgent", "otp", "kyc",
        "account", "refund", "pay", "click", "link"
    ]

    score = sum(1 for word in keywords if word in message.lower())
    is_scam = score >= 2
    confidence = min(0.95, 0.4 + score * 0.1)

    return is_scam, confidence
