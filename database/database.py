import json
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "scamshield"),
        connection_timeout=5
    )

def _fetch_all(query, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        cursor.close()
        return rows
    finally:
        conn.close()

def get_rules():
    try:
        rows = _fetch_all("SELECT id, rule_key, label, pattern, weight, explanation, advice FROM scam_rules WHERE enabled = 1 ORDER BY weight DESC")
        return rows
    except Error:
        # A clear error will be shown by /api/health; fallback keeps the scanner usable for demos.
        from detector import DEFAULT_RULES
        return DEFAULT_RULES

def get_samples():
    try:
        rows = _fetch_all("SELECT id, title, message, expected_risk, description FROM sample_messages ORDER BY id")
        return rows
    except Error:
        return [
            {"id": 1, "title": "UPI PIN Cashback Trap", "message": "Congratulations! You received Rs 4,999 cashback. Enter your UPI PIN at http://example.invalid/cashback to claim your reward.", "expected_risk": "HIGH", "description": "A PIN request and suspicious link are warning signs."},
            {"id": 2, "title": "Electricity Disconnection Panic", "message": "URGENT: Your electricity will be disconnected today. Call this number immediately and share OTP to stop disconnection.", "expected_risk": "HIGH", "description": "Urgency and OTP requests are warning signs."},
            {"id": 3, "title": "Bank KYC Threat", "message": "Your bank KYC will expire. Click this link immediately to update your account or it will be blocked.", "expected_risk": "MEDIUM", "description": "A threatening account notice with a link needs verification."},
            {"id": 4, "title": "Fake Screenshot Transfer Claim", "message": "Payment sent. Here is my screenshot. Give me the item now; bank confirmation may take time.", "expected_risk": "MEDIUM", "description": "Verify payment inside your own banking app."},
            {"id": 5, "title": "Genuine Bank Debit Alert", "message": "Your account has been debited by Rs 500. If you did not make this transaction, contact your bank using the official app or number.", "expected_risk": "LOW", "description": "A neutral alert with safe official-channel advice."},
            {"id": 6, "title": "OTP Safety Notice", "message": "Never share your OTP, UPI PIN, or password with anyone. Bank staff will never ask for these details.", "expected_risk": "LOW", "description": "This message gives protective advice."}
        ]

def get_quiz_questions():
    try:
        rows = _fetch_all("SELECT id, question, options_json, correct_answer, explanation FROM quiz_questions ORDER BY id")
        for row in rows:
            row["options"] = json.loads(row.pop("options_json"))
        return rows
    except (Error, ValueError):
        return [
            {"id": 1, "question": "A buyer sends a QR code and asks you to enter your UPI PIN to receive money. What should you do?", "options": ["Scan it and enter PIN", "Do not enter PIN; receiving money does not require it", "Share OTP instead"], "correct_answer": 1, "explanation": "A UPI PIN authorizes payments from your account; it is not needed to receive money."},
            {"id": 2, "question": "A caller says your bank account will be blocked unless you share an OTP. What is safest?", "options": ["Share it quickly", "Ask for their employee ID, then share it", "Do not share it; contact the bank through an official channel"], "correct_answer": 2, "explanation": "Never share OTPs. Contact your bank using its official app, card, or website."},
            {"id": 3, "question": "A buyer shows a payment screenshot. What should you do before handing over goods?", "options": ["Trust the screenshot", "Verify the credit in your own bank app", "Ask them to send another screenshot"], "correct_answer": 1, "explanation": "Screenshots can be edited. Confirm the transaction in your own bank account."}
        ]
