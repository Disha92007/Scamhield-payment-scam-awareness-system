import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from database import get_connection, get_rules, get_samples, get_quiz_questions
from detector import analyze_message

load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Please enter a message to analyze."}), 400
    if len(message) > 4000:
        return jsonify({"error": "Message must be 4,000 characters or fewer."}), 400
    return jsonify(analyze_message(message, get_rules()))

@app.get("/api/samples")
def api_samples():
    return jsonify(get_samples())

@app.get("/api/rules")
def api_rules():
    return jsonify(get_rules())

@app.get("/api/quiz")
def api_quiz():
    # Do not send correct answers to the browser before a response is submitted.
    questions = get_quiz_questions()
    return jsonify([{"id": q["id"], "question": q["question"],
                     "options": q["options"]} for q in questions])

@app.post("/api/quiz/answer")
def api_quiz_answer():
    data = request.get_json(silent=True) or {}
    question_id = data.get("question_id")
    answer = data.get("answer")
    try:
        question_id = int(question_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid question."}), 400
    for question in get_quiz_questions():
        if question["id"] == question_id:
            correct = str(answer) == str(question["correct_answer"])
            return jsonify({"correct": correct, "explanation": question["explanation"],
                            "correct_answer": question["correct_answer"]})
    return jsonify({"error": "Question not found."}), 404

@app.get("/api/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return jsonify({"status": "ok", "database": "connected"})
    except Exception:
        return jsonify({"status": "degraded", "database": "unavailable"}), 503

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
