# ScamShield — Payment Scam Awareness System

A college full-stack project built with HTML, CSS, JavaScript, Python Flask, and MySQL.

## Features
- Rule-based suspicious message scanner with risk level, score, matched indicators, explanations, and safety advice.
- Preloaded test samples.
- Four golden payment safety rules.
- Interactive quiz whose correct answers are checked by Flask.
- Cybercrime helpline and official reporting portal information.
- Message text is processed in memory and is not stored in the database.

> Educational project only. It does not guarantee scam detection. Never enter real OTPs, PINs, passwords, or financial credentials into a demo.

## Requirements
- Python 3.10+
- MySQL Server 8+
- VS Code (recommended)
- Python extension for VS Code

## Setup on Windows
1. Install Python and MySQL Server. Remember the MySQL password you set.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal and create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\\Scripts\\activate.bat
   ```
4. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and set `DB_PASSWORD` to your MySQL password.
6. Create the database and seed data. In MySQL Workbench, open `database/schema.sql` and execute the entire script. Alternatively:
   ```powershell
   mysql -u root -p < database/schema.sql
   ```
   Enter your MySQL password when prompted. If `mysql` is not recognized, run the script in MySQL Workbench.
7. Start the application:
   ```powershell
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in Chrome.

## Test
- Click any sample message, then press Analyze Message.
- Try: `Your account will be blocked today. Share OTP immediately at http://example.invalid`
- Scroll down and complete the quiz.
- Visit `http://127.0.0.1:5000/api/health` to check database connectivity.

## API endpoints
- `GET /api/health` — server/database status
- `POST /api/analyze` — body: `{"message":"..."}`
- `GET /api/samples` — sample test messages
- `GET /api/rules` — active detection rules
- `GET /api/quiz` — quiz questions without answers
- `POST /api/quiz/answer` — body: `{"question_id":1,"answer":1}`

## Privacy and limitations
The app does not write submitted message text to MySQL. Avoid adding request-body logging or analytics that capture messages. The scanner uses simple regex heuristics, not an AI model or a bank's fraud system. A LOW result does not mean a message is safe. Use official bank channels to verify.
