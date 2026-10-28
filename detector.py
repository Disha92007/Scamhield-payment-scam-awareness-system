import re

DEFAULT_RULES = [
    {"id": 1, "rule_key": "pin_request", "label": "UPI PIN or payment PIN request", "pattern": r"\b(enter|share|send|tell|provide)\b.{0,45}\b(upi\s*)?pin\b|\bpin\b.{0,35}\b(receive|claim|refund|cashback)\b", "weight": 5, "explanation": "A UPI PIN authorizes money leaving your account; it is not needed to receive money.", "advice": "Never enter your UPI PIN to receive a payment or refund."},
    {"id": 2, "rule_key": "otp_request", "label": "OTP or verification code request", "pattern": r"\b(share|send|tell|provide|verify with)\b.{0,35}\b(otp|one[- ]time password|verification code)\b", "weight": 4, "explanation": "A request to share an OTP can let someone authorize access or a transaction.", "advice": "Never share an OTP with callers or message senders."},
    {"id": 3, "rule_key": "urgent_threat", "label": "Urgency or threat", "pattern": r"\b(urgent|immediately|within \d+ hours|today only|account.{0,15}blocked|disconnect(ed|ion)?|will be blocked|suspended)\b", "weight": 2, "explanation": "Scammers often create panic so people act without verifying.", "advice": "Pause and independently contact the organization using its official channel."},
    {"id": 4, "rule_key": "suspicious_link", "label": "Link or shortened URL", "pattern": r"(https?://|www\.|bit\.ly|tinyurl|t\.co/|cutt\.ly)", "weight": 2, "explanation": "Unexpected links can lead to fake login pages or malicious sites.", "advice": "Do not open unexpected links. Visit the official website or app yourself."},
    {"id": 5, "rule_key": "reward_bait", "label": "Prize, cashback or reward bait", "pattern": r"\b(cashback|prize|lottery|won|reward|claim.{0,20}(money|cash|gift)|free gift)\b", "weight": 2, "explanation": "Unexpected rewards may be used to persuade people to click a link or disclose details.", "advice": "Verify offers in the official app; never pay a fee or reveal a PIN to claim money."},
    {"id": 6, "rule_key": "kyc_threat", "label": "KYC or account-block threat", "pattern": r"\b(kyc|account).{0,45}\b(expire|update|block(ed)?|suspend(ed)?)\b|\b(update|complete)\b.{0,20}\bkyc\b", "weight": 2, "explanation": "Fake KYC notices commonly pressure people to click a link or provide personal information.", "advice": "Check KYC status only through your bank's official app, branch, or website."},
    {"id": 7, "rule_key": "remote_access", "label": "Remote-access app request", "pattern": r"\b(anydesk|teamviewer|remote access|screen sharing app)\b", "weight": 4, "explanation": "Remote access can expose your screen, messages, and financial activity.", "advice": "Do not install remote-access apps at a stranger's request or share your screen during a payment."},
    {"id": 8, "rule_key": "qr_receive", "label": "QR code to receive money", "pattern": r"\b(scan|scanning)\b.{0,40}\b(qr|code)\b.{0,55}\b(receive|get|claim)\b|\b(qr code)\b.{0,55}\b(pin|payment)\b", "weight": 4, "explanation": "Scanning a QR code and entering a UPI PIN generally authorizes a payment, not receipt of money.", "advice": "Do not scan a stranger's QR code or enter a PIN to receive money."}
]

def analyze_message(message, rules=None):
    rules = rules or DEFAULT_RULES
    detected = []
    score = 0
    text = message.lower()
    for rule in rules:
        try:
            matched = re.search(rule["pattern"], text, re.IGNORECASE) is not None
        except (re.error, TypeError):
            matched = False
        if matched:
            score += int(rule.get("weight", 1))
            detected.append({
                "key": rule.get("rule_key", "indicator"),
                "label": rule.get("label", "Suspicious indicator"),
                "explanation": rule.get("explanation", "This pattern can be a warning sign."),
                "advice": rule.get("advice", "Verify independently using an official channel.")
            })
    score = min(score, 10)
    if score >= 6:
        risk = "HIGH"
        summary = "Several strong warning signs were found."
        advice = "Do not click links, share credentials, or send money. Verify through the official bank/app."
    elif score >= 3:
        risk = "MEDIUM"
        summary = "Some warning signs were found. Verify before acting."
        advice = "Pause and independently verify the sender and request."
    else:
        risk = "LOW"
        summary = "Few known warning signs were detected; this does not prove the message is safe."
        advice = "Stay cautious. Never share your PIN, password, or OTP, even if a message looks genuine."
    return {"risk": risk, "score": score, "summary": summary, "advice": advice,
            "indicators": detected, "disclaimer": "Educational rule-based screening only. It can miss scams or flag legitimate messages; it is not a guarantee of safety."}
