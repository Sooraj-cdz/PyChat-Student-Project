import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-production")
DATABASE = os.environ.get("DATABASE_PATH", "chat.db")

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            return render_template("index.html", error="Please enter a username.")
        session["username"] = username[:24]
        return render_template("chat.html", username=session["username"])
    if session.get("username"):
        return render_template("chat.html", username=session["username"])
    return render_template("index.html")

@app.post("/logout")
def logout():
    session.clear()
    return ("", 204)

@app.get("/api/messages")
def get_messages():
    if not session.get("username"):
        return jsonify({"error": "Please join the chat first."}), 401
    after_id = request.args.get("after", "0")
    try:
        after_id = max(0, int(after_id))
    except ValueError:
        after_id = 0
    with get_db() as db:
        rows = db.execute(
            "SELECT id, username, message, created_at FROM messages WHERE id > ? ORDER BY id ASC LIMIT 100",
            (after_id,)
        ).fetchall()
    return jsonify([dict(row) for row in rows])

@app.post("/api/messages")
def send_message():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Please join the chat first."}), 401
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400
    if len(message) > 1000:
        return jsonify({"error": "Messages must be 1,000 characters or fewer."}), 400

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO messages (username, message, created_at) VALUES (?, ?, ?)",
            (username, message, created_at)
        )
        message_id = cursor.lastrowid
    return jsonify({
        "id": message_id, "username": username,
        "message": message, "created_at": created_at
    }), 201

@app.get("/health")
def health():
    return jsonify({"status": "ok", "application": "PyChat"})

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
